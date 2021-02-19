import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import db.dbwrapper as dbw

def get_latest_price_date_for_symbol(symbol):
    with dbw.dbEngine.connect() as conn:

        results = conn.execute("""
                                SELECT max(dt) as max_date 
                                from asset_price 
                                join asset on asset.id = asset_price.asset_id 
                                where asset.symbol = %s 
                                """,
                                symbol)
        
        if results.rowcount == 1:
            result = results.fetchone()
            return result['max_date']
        
        return None

def get_latest_price_date():
    with dbw.dbEngine.connect() as conn:
    
        results = conn.execute("""
                                SELECT max(dt) as max_date
                                from asset_price
                                """)

        if results.rowcount == 1:
            result = results.fetchone()
            return result['max_date']
        
        return None