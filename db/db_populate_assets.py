import sys
sys.path.append('/app')
import dbwrapper as dbw
import data.polygon as d_poly
import data.alpaca as d_alpaca

USE_POLYGON = False

def alpaca_populate_assets():
    with dbw.dbEngine.connect() as conn:
  
        #all the existing symbols and flags so that we don't add ones that already exist
        result = conn.execute("""SELECT symbol, id FROM asset""")
        symbols = [row['symbol'] for row in result]

        assets = d_alpaca.get_all_assets()

        for asset in assets:
            try:
                if asset.status == 'active' and asset.tradable:
                    if asset.symbol not in symbols:
                        print(f"Alpaca New asset: {asset.symbol} {asset.name}")
                        conn.execute("""INSERT INTO asset (exchange, symbol, name, source, easy_to_borrow, marginable, shortable) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                        (asset.exchange, asset.symbol, asset.name, 'alpaca', asset.easy_to_borrow, asset.marginable, asset.shortable))
                    else:
                        conn.execute("""UPDATE asset SET easy_to_borrow = %s, marginable = %s, shortable = %s where symbol = %s""", 
                        (asset.easy_to_borrow, asset.marginable, asset.shortable, asset.symbol))
            except Exception as e:
                print(asset.symbol)
                print(e)

def polygon_populate_assets():
    with dbw.dbEngine.connect() as conn:
        #all the existing symbols and flags so that we don't add ones that already exist
        result = conn.execute("""SELECT symbol, id FROM asset""")
        symbols = [row['symbol'] for row in result]

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

dbw.initDb()

if USE_POLYGON:
    polygon_populate_assets()
alpaca_populate_assets()