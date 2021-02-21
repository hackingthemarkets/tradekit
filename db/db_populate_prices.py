#!/usr/bin/env python 
 
import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta, timezone

from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor

import data.polygon as d_poly
import data.alpaca as d_alpaca
import dbwrapper as dbw
from sqlalchemy import exc
import pandas as pd

MAX_WORKERS = 20

DAYS_BACK = 7
PERIOD = 'day'
MULTIPLIER = 1

# Can be polygon or alpaca
DATA_SOURCE = 'alpaca'
# Chunk size only applies to alpaca
CHUNK_SIZE = 200

symbolsToFetch = Queue()

def writeAssetPrice(conn, symbol, source, priceData):
    try:
        conn.execute("""INSERT INTO asset_price (asset_id, source, dt, timespan, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
        priceData['asset_id'], source, priceData['t'], PERIOD, priceData['o'], priceData['h'], priceData['l'], priceData['c'], priceData['v'])
    except exc.SQLAlchemyError as e:
        print(e)

def fetchSymbolBars(symbol, source, from_date, to_date):
    priceDataSet = []

    if source == 'polygon':
        bars = d_poly.get_agg_bars(symbol['symbol'], PERIOD, MULTIPLIER, from_date, to_date)
        if bars is not None:
            # print('Got barsets for symbol {} {}'.format(symbol, bars))
            for bar in bars:
                pData = bar.copy()
                pData['t'] = d_poly.ts_to_datetime(bar['t'])
                pData['symbol'] = symbol['symbol']
                pData['asset_id'] = symbol['asset_id']
                priceDataSet.append(pData)
        else:
            print('No bars found for {}'.format(symbol['symbol']))

    elif source == 'alpaca':
        # symbol is a chunk
        symbols = list(map(getSymbolName, symbol))
        api = d_alpaca.get_api_pointer()
        
        barsets = d_alpaca.get_barset(api, symbols, PERIOD, from_date.isoformat())
        if barsets is not None:
            for bs in barsets:
                for bar in barsets[bs]:
                    pData = {
                        "t": bar.t.date(),
                        "o": bar.o,
                        "h": bar.h,
                        "l": bar.l,
                        "c": bar.c,
                        "v": bar.v,
                        "symbol": bs,
                        "asset_id": asset_dict[bs]
                    }

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
        from_date = datetime.now(tz=timezone.utc) - timedelta(days=DAYS_BACK)
        to_date = datetime.now(tz=timezone.utc)
    else:
        print('Error: Data source ({}) is not valid'.format(DATA_SOURCE))
        return

    try:
        fetchSymbolBars(symbol, DATA_SOURCE, from_date, to_date)
    except:
        e = sys.exc_info()[0]
        print(e)

def symbolFeeder(threadPool):
    while symbolsToFetch.qsize() > 0:
        try:
            symbol = symbolsToFetch.get()
            threadPool.submit(fetchSymbol, symbol)
        except Empty:
            return
        except:
            e = sys.exc_info()[0]
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
    to_date = datetime.now(tz=timezone.utc)
    from_date = datetime.now(tz=timezone.utc) - timedelta(days=DAYS_BACK)

    symbols = []
    global asset_dict
    asset_dict = {}

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
            
            asset_dict[row['symbol']] = row['id']
            symbols.append(symbol)

    return symbols

dbw.initDb()
buildSymbolQueue()