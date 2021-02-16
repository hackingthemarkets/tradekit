import psycopg2
from sqlalchemy import engine
from sqlalchemy import create_engine
import json

dbConfig = {}
dbEngine = {}

def initDbConfig():
    with open('server.json') as json_file:
        serverConfig = json.load(json_file)

    global dbConfig

    dbConfig = serverConfig['db']['development']['connection']

    print('Host: ' + dbConfig['host'])
    print('Port: ' + str(dbConfig['port']))
    print('Database: ' + dbConfig['database'])
    print('User: ' + dbConfig['user'])

def initDb():
    global dbEngine

    connect_url = engine.url.URL(
        'postgresql+psycopg2', 
        username=dbConfig['user'],
        password=dbConfig['password'],
        host=dbConfig['host'],
        port=dbConfig['port'],
        database=dbConfig['database']
    )
    dbEngine = create_engine(connect_url)

    with dbEngine.connect() as conn:
        result = conn.execute('SELECT version()')
        for row in result:
            print(row)

def transaction(connection):
    if not connection.in_transaction():
        with connection.begin():
            yield connection
    else:
        yield connection