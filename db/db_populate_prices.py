import sqlite3
import alpaca_trade_api as trade_api
from config import *
from datetime import date
import tulipy, numpy

#get all assets and prep them up
connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM asset
""")

rows = cursor.fetchall()
symbols = []
asset_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    asset_dict[symbol] = row['id']

api = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_END_POINT)

#symbols = ['MSFT'] #for testing on 1

#last 100 days, since we are getting daily values
chunk_size = 100
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day', after=date.today().isoformat())
    for symbol in barsets:
        #print(f"processing symbol {symbol}")
        #to compute tulip indicators we need a list for numpy array
        recent_closes = [bar.c for bar in barsets[symbol]]
    
        for bar in barsets[symbol]:
            asset_id = asset_dict[symbol]

            #compute the indicators only for the last day
            if len(recent_closes)>=50 and date.today().isoformat() == bar.t.date().isoformat():
                sma_20 = tulipy.sma(numpy.array(recent_closes), period = 20)[-1]
                sma_50 = tulipy.sma(numpy.array(recent_closes), period = 50)[-1]
                rsi_14 = tulipy.rsi(numpy.array(recent_closes), period = 14)[-1]
            else:
                sma_20, sma_50, rsi_14 = None, None, None

            cursor.execute("""
                INSERT INTO asset_price (asset_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (asset_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))

connection.commit()