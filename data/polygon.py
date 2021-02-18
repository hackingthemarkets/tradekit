import sys
sys.path.append('/app')
from data.api_data import POLYGON_API_KEY
import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import math

# URL for all the tickers on Polygon
POLYGON_TICKERS_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'

def get_all_tickers():
    page = 1

    session = requests.Session()
    # Initial request to get the ticker count
    r = session.get(POLYGON_TICKERS_URL.format(page, POLYGON_API_KEY))
    data = r.json()

    count = data['count']
    print('total tickers ' + str(count))
    pages = math.ceil(count / data['perPage'])

    #tickers = pd.DataFrame()
    tickers = []
    #for pages in range (2, pages+1):
    for pages in range (2, 4): #for testing otherwise too long
        r = session.get(POLYGON_TICKERS_URL.format(page, POLYGON_API_KEY))
        data = r.json()
        #tickers = df.append(pd.DataFrame(data['tickers']))
        tickers = tickers + data['tickers']
        page += 1 
    
    return tickers

def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')
