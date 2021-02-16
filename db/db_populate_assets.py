import os
import json
from common.dbwrapper import *
import alpaca_trade_api as trade_api
from config import *

initDbConfig()

with dbEngine.connect() as conn:
    result = conn.execute('SELECT symbol, name FROM asset')
    symbols = [row['symbol'] for row in result.rows]

    api = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY,
                        base_url=ALPACA_END_POINT)
    assets = api.list_assets()

    for asset in assets:
        try:
            if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
                print(f"New asset {asset.symbol} {asset.name}")
                conn.execute("INSERT INTO asset (alpaca_id, exchange, symbol, name) VALUES (?, ?, ?, ?)",
                            (asset.id, asset.exchange, asset.symbol, asset.name))
        except Exception as e:
            print(asset.symbol)
            print(e)