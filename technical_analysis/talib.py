import sys
sys.path.append('/app')
import db.dbwrapper as dbw
import talib
import pandas as pd
from technical_analysis.talib_candelstick_patterns import patterns

def get_all_patterns():
    return patterns

def get_last_pattern_dir_for_symbol(symbol, pattern:str):
    with dbw.dbEngine.connect() as conn:
        
        df = pd.read_sql("""
        SELECT * from asset_price
        JOIN asset on asset.id = asset_price.asset_id
        where asset.symbol = %s
        """, conn, params = [symbol])

        pattern_function = getattr(talib, pattern)
        if len(df) > 0:
            try:
                result = pattern_function(df['open'], df['high'], df['low'], df['close'])
                last = result.tail(1).values[0]
                if last > 0:
                    return 'bullish'
                elif last < 0:
                    return 'bearish'
                else:
                    return None
            except:
                return None