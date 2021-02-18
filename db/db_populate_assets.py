import sys
sys.path.append('/app')
import os
import json
import pprint
import dbwrapper as dbw
import alpaca_trade_api as trade_api
import pandas as pd
import data.polygon as d_poly
import data.alpaca as alpaca

dbw.initDb()

with dbw.dbEngine.connect() as conn:
    #all the existing symbols and flags so that we don't add ones that already exist
    result = conn.execute("""SELECT symbol, id FROM asset""")
    symbols = [row['symbol'] for row in result]

    #first pass using polygon since it has a full univerise
    assets = d_poly.get_all_tickers()

    for asset in assets:
        try:
            if asset['active'] == True and asset['ticker'] not in symbols:
                print(f"Polygon New asset {asset['primaryExch']} {asset['ticker']} {asset['name']} {asset['market']} {asset['locale']} {asset['currency']}")
                #type is included at times
                if 'type' not in asset:
                    conn.execute("""
                        INSERT INTO asset (exchange, symbol, name, market, locale, currency, source) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (asset['primaryExch'], asset['ticker'], asset['name'], asset['market'], asset['locale'], asset['currency'],'polygon'))
                else:
                    conn.execute("""
                        INSERT INTO asset (exchange, symbol, name, market, locale, currency, source, type) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (asset['primaryExch'], asset['ticker'], asset['name'], asset['market'], asset['locale'], asset['currency'],'polygon', asset['type']))
        except Exception as e:
            print(asset['ticker'])
            print(e)

    #Alpca mainly for flags, but just in case we need to add missing ones
    al_assets = alpaca.get_all_assets()
    
    #since it runs back-to-back, let's refresh after polygon
    result = conn.execute("""SELECT symbol, id FROM asset""")
    symbols = [row['symbol'] for row in result]

    for al_asset in al_assets:
        try:
            if al_asset.status == 'active' and al_asset.tradable:
                if al_asset.symbol not in symbols:
                    print(f"Alpaca New asset: {al_asset.symbol} {al_asset.name}")
                    conn.execute("""INSERT INTO asset (exchange, symbol, name, source, easy_to_borrow, marginable, shortable) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                    (al_asset.exchange, al_asset.symbol, al_asset.name, 'alpaca', al_asset.easy_to_borrow, al_asset.marginable, al_asset.shortable))
                else:
                    conn.execute("""UPDATE asset SET easy_to_borrow = %s, marginable = %s, shortable = %s where symbol = %s""", 
                    (al_asset.easy_to_borrow, al_asset.marginable, al_asset.shortable, al_asset.symbol))
        except Exception as e:
            print(al_asset.symbol)
            print(e)