import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import db.dbwrapper as dbw


def get_symbols_close_highest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    max(CLOSE) AS CLOSE
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.close = ap.close
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_close_lowest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    min(CLOSE) AS CLOSE
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.close = ap.close
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_intra_highest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    max(high) AS high
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.high = ap.high
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_intra_lowest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    min(low) AS low
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.low = ap.low
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_volume_highest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    max(volume) AS volume
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.volume = ap.volume
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_volume_lowest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    min(volume) AS volume
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.volume = ap.volume
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()
    

def get_symbols_open_highest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    max(open) AS open
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.open = ap.open
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

def get_symbols_open_lowest_on_date(on_date:date):
    with dbw.dbEngine.connect() as conn:
        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                    JOIN (
                                        SELECT
                                            ap.asset_id
                                        FROM
                                            asset_price ap
                                            JOIN (
                                                SELECT
                                                    asset_id,
                                                    min(open) AS open
                                                FROM
                                                    asset_price
                                                where timespan = 'day'
                                                GROUP BY
                                                    asset_id) AS tar ON tar.asset_id = ap.asset_id
                                                AND tar.open = ap.open
                                            WHERE
                                                date(dt) = %s and ap.timespan = 'day') AS ap ON ap.asset_id = asset.id
                                """,
                                on_date.isoformat())
        return results.fetchall()

