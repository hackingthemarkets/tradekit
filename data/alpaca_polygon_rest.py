import sys
sys.path.append('/app')
from data.api_data import ALPACA_API_KEY, ALPACA_END_POINT, ALPACA_SECRET_KEY
import alpaca_trade_api as trade_api

def get_agg_bars(symbol, period, multiplier, start, end):

    api = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_END_POINT)

    return api.polygon.historic_agg_v2(symbol, 1, period, _from=start, to=end)