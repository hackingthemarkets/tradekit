import sys
sys.path.append('/app')
from data.api_data import ALPACA_API_KEY
import websocket, json

POLYGON_ALPACA_WS = 'wss://alpaca.socket.polygon.io/stocks'
TICKERS_TO_STREAM = "Q.MSFT"

def on_open(ws):
    auth_data = {
        "action":"auth",
        "params": ALPACA_API_KEY
    }
    ws.send(json.dumps(auth_data))

    sub_data = {
        "action":"subscribe",
        "params":TICKERS_TO_STREAM
    }
    ws.send(json.dumps(sub_data))

def on_message(ws,message):
    print(message)

def on_close(ws):
    print("Conn Closed")

ws = websocket.WebSocketApp(POLYGON_ALPACA_WS, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()