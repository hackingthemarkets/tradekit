import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import db.dbwrapper as dbw

def get_all_strategies():
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    strategy
                                """)
        return results.fetchall()


def register_strategy_for_asset_id(asset_id, strategy_id):
    with dbw.dbEngine.connect() as conn:
        conn.execute("""
                        INSERT INTO asset_strategy(asset_id, strategy_id) VALUES (%s,%s)
                        """, asset_id, strategy_id)

def get_strategy_by_id(id):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    strategy
                                where id = %s
                                """, id)
        return results.fetchone()

def get_all_assets_by_strategy_id(strategy_id):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN asset_strategy ON asset_strategy.asset_id = asset.id
                                WHERE
                                    strategy_id = %s
                                """, strategy_id)
        return results.fetchall()