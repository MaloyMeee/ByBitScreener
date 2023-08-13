import _thread
import websocket
import json
import threading as th

class SocketConnection(websocket.WebSocketApp):
    def __init__(self, url, params=[]):
        super().__init__(url=url, on_open=self.on_open)

        self.params = params
        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, e: print('Error: ', e)
        self.on_close = lambda ws: print('Connection closed')

        self.run_forever()

    def on_open(self, ws,):
        print('WebSocket is opened')

        def run(*args):
            tradeStr = {"op": "subscribe", "args": self.params}
            ws.send(json.dumps(tradeStr))

        _thread.start_new_thread(run, ())

    def message(self, msg):
        print(msg)
th.Thread(target=SocketConnection,
          args=('wss://stream.bybit.com/v5/public/linear', [f"orderbook.50.BTCUSDT"], 'type=snapshot')).start()