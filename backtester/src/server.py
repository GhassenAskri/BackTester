from backtester.src.binance.session import client
import backtester.src.data_handler as dh
import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route("/get-data-btc")
def get_data_by_ticker():
    data = dh.save_all_data(client, tickers='BTCUSDT', save=False)
    print('Data loading finished')
    return data.to_html()

@app.route("/")
def hello():
    return "Hello Gaston: big up we made the first step"

if __name__ == "__main__":
    app.run(debug=True)


