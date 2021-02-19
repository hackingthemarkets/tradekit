import sys
sys.path.append('/app')
from datetime import datetime, date, timedelta
import db.dbwrapper as dbw

def get_all_active_symbols():
    with dbw.dbEngine.connect() as conn:

        results = conn.execute("""
                                SELECT
                                    *
                                FROM
                                    asset
                                WHERE
                                    active = TRUE
                                """)
        return results.fetchall()