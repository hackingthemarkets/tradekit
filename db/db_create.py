import os
import json
from dbwrapper import *

def initSchema():
    basepath = 'tables'
    entries = os.listdir(basepath)
    print('Initializing Schema')
    
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                print('Running '+ entry.name)
                # TODO: Can put this in a function and just yield entries intsead
                with open(entry, 'r') as sqlFile:
                    query = sqlFile.read()
                    with dbEngine.connect() as conn:
                        result = conn.execute(query)
    
    print('Done initializing')

initDbConfig()
initDb()
initSchema()

# #seed future strategies here
# strategies = ['opening_range_breakout', 'opening_range_breakdown']

# for strategy in strategies:
#     cursor.execute("""
#         INSERT INTO strategy (name) VALUES (?)
#     """, (strategy,))

# connection.commit()