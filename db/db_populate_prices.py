import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import tulipy, numpy
import data.polygon as d_poly
import dbwrapper as dbw

DAYS_BACK = 365
PERIOD = 'day'
MULTIPLIER = 1

dbw.initDb()

with dbw.dbEngine.connect() as conn:
    #getting and prepping symbols to get bars for
    results = conn.execute("""SELECT symbol, id FROM asset""")

    symbols = []
    asset_dict = {}
    
    for row in results:
        symbol = row['symbol']
        symbols.append(symbol)
        asset_dict[symbol] = row['id']

    #specify default to and from
    to_date = datetime.now()
    from_date = datetime.now() - timedelta(days=DAYS_BACK)

    #get the max data we have in the db to adjust from if need be
    max_dates = conn.execute("""select Max(dt) as dt from asset_price""")

    for row in max_dates:
        if row[0] is not None:
            #start from the next day
            from_date = row[0] + timedelta(days=1)


    for symbol in symbols:
        bars = d_poly.get_agg_bars(symbol, PERIOD, MULTIPLIER, from_date, to_date)
        if bars is not None:
            #recent_closes = [bar['c'] for bar in bars]
            print('bars received')
            asset_id = asset_dict[symbol]
            for bar in bars:
                conn.execute("""INSERT INTO asset_price (asset_id, source, dt, timespan, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                asset_id, 'polygon', d_poly.ts_to_datetime(bar['t']), PERIOD, bar['o'], bar['h'], bar['l'], bar['c'], bar['v'])
        

# #api = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_END_POINT)

# #symbols = ['MSFT'] #for testing on 1

# #last 100 days, since we are getting daily values
# chunk_size = 100
# for i in range(0, len(symbols), chunk_size):
#     symbol_chunk = symbols[i:i+chunk_size]
#     barsets = api.get_barset(symbol_chunk, 'day', after=date.today().isoformat())
#     for symbol in barsets:
#         #print(f"processing symbol {symbol}")
#         #to compute tulip indicators we need a list for numpy array
#         recent_closes = [bar.c for bar in barsets[symbol]]
    
#         for bar in barsets[symbol]:
#             asset_id = asset_dict[symbol]

#             #compute the indicators only for the last day
#             if len(recent_closes)>=50 and date.today().isoformat() == bar.t.date().isoformat():
#                 sma_20 = tulipy.sma(numpy.array(recent_closes), period = 20)[-1]
#                 sma_50 = tulipy.sma(numpy.array(recent_closes), period = 50)[-1]
#                 rsi_14 = tulipy.rsi(numpy.array(recent_closes), period = 14)[-1]
#             else:
#                 sma_20, sma_50, rsi_14 = None, None, None

#             cursor.execute("""
#                 INSERT INTO asset_price (asset_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (asset_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))

# connection.commit()