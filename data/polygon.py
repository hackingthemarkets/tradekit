import sys
sys.path.append('/app')
from data.api_data import POLYGON_API_KEY
from datetime import datetime, date, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import math

# URL for all the tickers
POLYGON_TICKERS_URL = 'https://api.polygon.io/v2/reference/tickers?page={}&apiKey={}'

# URL for aggregate data - default limit 5000. Adjusted for splits and dividents
POLYGON_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?unadjusted=false&sort=asc&apiKey={}'

# URL For specific, but it looks like they are all served by the same endpoint, regardless of the type
POLYGON_STOCKS_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?unadjusted=false&sort=asc&apiKey={}'
POLYGON_FOREX_AGGS_URL  = 'https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?unadjusted=false&sort=asc&apiKey={}'
POLYGON_CRYPTO_AGGS_URL = 'https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?unadjusted=false&sort=asc&apiKey={}'

def get_agg_bars(symbol, period, multiplier, start, end):
    session = requests.Session()
    try:
        r = session.get(POLYGON_AGGS_URL.format(symbol, multiplier, period, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), POLYGON_API_KEY))
        if r:
            data = r.json()
            return data['results']
        return None
    except Exception as e:
        print('****** getting bars errored for symbol: ' + str(symbol))
        print(e, data)
        return None

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
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')
