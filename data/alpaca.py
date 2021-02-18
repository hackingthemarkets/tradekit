import sys
sys.path.append('/app')
from data.api_data import ALPACA_API_KEY, ALPACA_END_POINT, ALPACA_SECRET_KEY
import alpaca_trade_api as trade_api

def get_all_assets():
    
    api = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_END_POINT)

    return api.list_assets()
