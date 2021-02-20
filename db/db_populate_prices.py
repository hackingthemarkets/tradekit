#!/usr/bin/env python 
 
import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta

from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

import data.polygon as d_poly
import data.alpaca as d_alpaca
import dbwrapper as dbw

MAX_WORKERS = 20

DAYS_BACK = 3
PERIOD = 'day'
MULTIPLIER = 1

# Can be polygon or alpaca
DATA_SOURCE = 'alpaca'
# Chunk size only applies to alpaca
CHUNK_SIZE = 200

symbolsToFetch = Queue()

def writeAssetPrice(conn, symbol, source, priceData):
    conn.execute("""INSERT INTO asset_price (asset_id, source, dt, timespan, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
    symbol['asset_id'], source, priceData['t'], PERIOD, priceData['o'], priceData['h'], priceData['l'], priceData['c'], priceData['v'])

def fetchSymbolBars(symbol, source, from_date, to_date):
    priceDataSet = []

    if source == 'polygon':
        bars = d_poly.get_agg_bars(symbol['symbol'], PERIOD, MULTIPLIER, from_date, to_date)
        if bars is not None:
            # print('Got barsets for symbol {} {}'.format(symbol, bars))
            for bar in bars:
                pData = bar.copy()
                pData['t'] = d_poly.ts_to_datetime(bar['t'])
                priceDataSet.append(pData)
        else:
            print('No bars found for {}'.format(symbol['symbol']))

    elif source == 'alpaca':
        # symbol is a chunk
        symbols = list(map(getSymbolName, symbol))
        api = d_alpaca.get_api_pointer()
        bars = d_alpaca.get_barset(api, symbols, PERIOD, from_date)
        if bars is not None:
            # print('Got barsets for symbol {} {}'.format(symbols, bars))
            for bar in bars:
                pData = bar.copy()
                priceData['t'] = bar.t.date()
                priceDataSet.append(pData)
        else:
            print('No bars found for {}'.format(symbols))
            
    else:
        print('Error: Data source ({}) is not valid'.format(source))
        return
    
    with dbw.dbEngine.connect() as conn:
        for priceData in priceDataSet:
            writeAssetPrice(conn, symbol, source, priceData)

def fetchSymbol(symbol):

    if DATA_SOURCE == 'polygon':
        from_date = symbol['from_date']
        to_date = symbol['to_date']
    elif DATA_SOURCE == 'alpaca': 
        from_date = datetime.now() - timedelta(days=DAYS_BACK)
        to_date = datetime.now()
    else:
        print('Error: Data source ({}) is not valid'.format(DATA_SOURCE))
        return

    try:
        fetchSymbolBars(symbol, DATA_SOURCE, from_date, to_date)
    except Exception as e:
        print(e)

def symbolFeeder(threadPool):
    while symbolsToFetch.qsize() > 0:
        try:
            symbol = symbolsToFetch.get()
            threadPool.submit(fetchSymbol, symbol)
        except Empty:
            return
        except Exception as e:
            print('Exception with {}'.format(symbol))
            print(e)
            continue

def buildSymbolQueue():
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    symbols = get_symbols_dictionary()

    if DATA_SOURCE == 'polygon':
        for s in symbols:
            symbolsToFetch.put(s)
    elif DATA_SOURCE == 'alpaca': 
        symbolChunks = list(chunks(symbols, CHUNK_SIZE))
        for sc in symbolChunks:
            symbolsToFetch.put(sc)
    else:
        print('Error: Data source ({}) is not valid'.format(DATA_SOURCE))
        return

    symbolFeeder(threadPool=pool)
    pool.shutdown(wait=True)

def getSymbolName(s):
    return s['symbol']

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_symbols_dictionary():
    to_date = datetime.now()
    from_date = datetime.now() - timedelta(days=DAYS_BACK)

    with dbw.dbEngine.connect() as conn:
        #getting and prepping symbols to get bars for
        results = conn.execute("""
            SELECT 
                symbol, 
                id,
                (SELECT MAX(dt) as dt from asset_price WHERE asset_price.asset_id = asset.id) as max_dt
            FROM asset 
            order by symbol
        """)

        symbols = []
        
        for row in results:
            symbol = {
                "symbol": row['symbol'], 
                "asset_id": row['id'], 
                "from_date": from_date, 
                "to_date": to_date
            }

            if row['max_dt'] is not None:
                #start from the next day
                symbol['from_date'] = row['max_dt'] + timedelta(days=1)
            
            symbols.append(symbol)
    return symbols

dbw.initDb()
buildSymbolQueue()
# if USE_POLYGON:
#     polygon_populate_prices()
# else: 
#     alpaca_populate_prices()