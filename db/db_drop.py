import sqlite3
from config import * 

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE asset_price
""")

cursor.execute("""
    DROP TABLE asset
""")

cursor.execute("""
    DROP TABLE strategy
""")

cursor.execute("""
    DROP TABLE asset_strategy
""")

connection.commit()