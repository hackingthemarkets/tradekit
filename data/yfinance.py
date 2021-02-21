import yfinance

def get_agg_daily_bars(symbol, start, end)
    return yfinance.download(symbol, start=start, end=end)
