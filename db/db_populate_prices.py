import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import data.polygon as d_poly
import data.alpaca as d_alpaca
import dbwrapper as dbw

DAYS_BACK = 365
PERIOD = 'day'
MULTIPLIER = 1

USE_POLYGON = False

def polygon_populate_prices():
    with dbw.dbEngine.connect() as conn:

        symbols, asset_dict = get_symbols_dictionary()
        to_date, from_date = get_to_from_dates()

        for symbol in symbols:
            bars = d_poly.get_agg_bars(symbol, PERIOD, MULTIPLIER, from_date, to_date)
            if bars is not None:
                asset_id = asset_dict[symbol]
                for bar in bars:
                    conn.execute("""INSERT INTO asset_price (asset_id, source, dt, timespan, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                    asset_id, 'polygon', d_poly.ts_to_datetime(bar['t']), PERIOD, bar['o'], bar['h'], bar['l'], bar['c'], bar['v'])

def alpaca_populate_prices():
    with dbw.dbEngine.connect() as conn:

        symbols, asset_dict = get_symbols_dictionary()
        to_date, from_date = get_to_from_dates()
        
        api = d_alpaca.get_api_pointer()

        chunk_size = 200
        for i in range(0, len(symbols), chunk_size):
            symbol_chunk = symbols[i:i+chunk_size]
            
            barsets = d_alpaca.get_barset(api,symbol_chunk, PERIOD, from_date)

            for symbol in barsets:
                for bar in barsets[symbol]:
                    asset_id = asset_dict[symbol]
                    conn.execute("""INSERT INTO asset_price (asset_id, source, dt, timespan, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                    asset_id, 'alpaca', bar.t.date(), PERIOD, bar.o, bar.h, bar.l, bar.c, bar.v)

def get_symbols_dictionary():
    with dbw.dbEngine.connect() as conn:
        #getting and prepping symbols to get bars for
        results = conn.execute("""SELECT symbol, id FROM asset""")

        symbols = []
        asset_dict = {}
        
        for row in results:
            symbol = row['symbol']
            symbols.append(symbol)
            asset_dict[symbol] = row['id']
    return symbols, asset_dict

#TODO: It might be better trying to get max dates per symbol, especially for polygon that uses a per symbol endpoint
def get_to_from_dates():
    with dbw.dbEngine.connect() as conn:
        #specify default to and from
        to_date = datetime.now()
        from_date = datetime.now() - timedelta(days=DAYS_BACK)

        #get the max data we have in the db to adjust from if need be
        max_dates = conn.execute("""select Max(dt) as dt from asset_price""")

        for row in max_dates:
            if row[0] is not None:
                #start from the next day
                from_date = row[0] + timedelta(days=1)
    return to_date, from_date

dbw.initDb()
if USE_POLYGON:
    polygon_populate_prices()
else: 
    alpaca_populate_prices()