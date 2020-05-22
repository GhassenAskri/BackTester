# from arctic import Arctic
import pandas as pd
from .BinanceKeys import BinanceKey1
from .binance.session import client
# from Data.Arctic import store
import time
import datetime
from .binance.enums import *
import matplotlib.pyplot as plt


def get_exchange_statut(client):
    # Get Status of Exchange & Account
    try:
        status = client.get_system_status()
        print("\nExchange Status: ", status)

        # Account Withdrawal History Info
        withdraws = client.get_withdraw_history()
        print("\nClient Withdraw History: ", withdraws)

        # get Exchange Info
        info = client.get_exchange_info()
        print("\nExchange Info (Limits): ", info)
    except():
        pass


def save_all_data(client, platform='BINANCE', tickers=None, save=True, start=0):
    # # Connect to Local MONGODB
    # store = Arctic('localhost')

    if save:
        if not platform in store.list_libraries():
            # Create the library - defaults to VersionStore
            store.initialize_library(platform)

        # Access the library
        library = store[platform]

    if tickers is None:
        # initialize the tickers list
        tickers = []
        # get all symbol prices
        prices = client.get_all_tickers()
        for i in range(len(prices)):
            tickers.append(prices[i]['symbol'])
    elif not isinstance(tickers, list):
        tickers = [tickers]
    """
        transforming data to a cleaned dataframe
    """
    for i in range(start, len(tickers)):
        # todo : try to find the earliest date for each ticker
        print(i, ' ticker : ', tickers[i])
        klines = client.get_historical_klines(tickers[i], client.KLINE_INTERVAL_1MINUTE, "1 May, 2020")
        data = pd.DataFrame(klines, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time',
                                             'Quote asset volume',
                                             'Number of trades', 'Taker buy base asset volume',
                                             'Taker buy quote asset volume', 'ignored'])
        data = data.drop(['ignored', 'Close_time'], axis=1)
        data['Date'] = data['Open_time']
        data['Open_time'] = data['Open_time'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
        data = data.set_index(['Open_time'])
        data = data.astype(float)

        if save:
            # Store the data in the library
            library.write(tickers[i], data, metadata={'source': platform})
        else:
            return data


def load_data(ticker, columns=['Close'], platform='BINANCE'):
    try:
        # Access the library
        library = store[platform]
        item = library.read(ticker).data
        if columns == 'all':
            return item.astype(float)
        elif columns == 'ohlcv':
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            return item[columns].astype(float)
        else:
            return item[columns].astype(float)
    except:
        raise ('Erreur du chargement ticker')

def load_from_platform(ticker, interval='1d', columns='ohlcv', plateform='Binance'):
    if plateform == 'Binance':
        klines = client.get_historical_klines(ticker, interval, "17 Aug 2017")
        data = pd.DataFrame(klines, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time',
                                            'Quote asset volume',
                                            'Number of trades', 'Taker buy base asset volume',
                                            'Taker buy quote asset volume', 'ignored'])
        data = data.drop(['ignored', 'Close_time'], axis=1)
        data['Open_time'] = data['Open_time'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
        data = data.set_index(['Open_time'])

        if columns == 'all':
            return data.astype(float)
        elif columns == 'ohlcv':
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            return data[columns].astype(float)
        else:
            return data[columns].astype(float)
        return data



if __name__ == '__main__':
    pass

    # client = Client(BinanceKey1['api_key'], BinanceKey1['api_secret'])
    #
    # # # get all symbol prices
    # # prices = client.get_all_tickers()
    #
    # # Connect to Local MONGODB
    # store = Arctic('localhost')
    #
    # # # Create the library - defaults to VersionStore
    # # store.initialize_library('BINANCE')
    #
    # # Access the library
    # library = store['BINANCE']
    #
    # # todo : loop this for all the tickers
    # #
    # # """
    # #     transforming data to a cleaned dataframe
    # # """
    # # for i in range(0, len(prices)):
    # #
    # #     #todo : try to find the earliest date for each ticker
    # #     ticker = prices[i]['symbol']
    # #     print(i, ' ticker : ', ticker)
    # #     klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_5MINUTE, "1 Dec, 2017")
    # #     data = pd.DataFrame(klines, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote asset volume',
    # #                'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'ignored'])
    # #     data = data.drop(['ignored', 'Close_time'], axis=1)
    # #     data['Open_time'] = data['Open_time'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
    # #     data = data.set_index(['Open_time'])
    # #
    # #     # Store the data in the library
    # #     library.write(ticker, data, metadata={'source': 'Binance'})
    # #
    #
    # # # Reading the data
    # # item = library.read("BTCUSDT")
    # # df_imported = item.data
    # # metadata = item.metadata
    # #
    # # plt.scatter(df_imported.index[:10], df_imported['Open'][0:10])
    # #
    # # plt.title("Temperature vs. Sold ice creams")
    # # plt.xlabel("Temperature")
    # # plt.ylabel("Sold ice creams count")
    # # plt.show()
    # load_data('BTCUSDT')
