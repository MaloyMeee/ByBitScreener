from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
from time import time
from config import api_key, api_secret
from cCoin import Coin
import threading as th


pd.set_option('display.max_rows', None)

session = HTTP(api_key=api_key, api_secret=api_secret, testnet=False)  # создание сессии


# session = HTTP(testnet=True)  # создание сессии


def get_all_tickers():  # все тикеры фьючерсов
    tickers = []
    symbol = session.get_instruments_info(
        category="linear",
        status="Trading",
        quoteCoin="USDT"
    )
    request = symbol.get('result').get('list')
    for i in request:
        tickers.append(i.get('symbol'))
    return tickers


def bidask(ask, bid, ticker):
    zero = pd.DataFrame({'price': ['-----'], 'volume': ['-----'], 'vol_usdt': [ticker]})
    bidask = pd.concat([ask, zero])
    bidask = pd.concat([bidask, bid])
    return bidask


def vyzov(ticker):
    ask = ticker.get_ask(ticker.ticker, ticker.limit)
    bid = ticker.get_bid(ticker.ticker, ticker.limit)
    filt_ask = ticker.filter_usdt_vol(ask, ticker.vol_usdt)
    filt_bid = ticker.filter_usdt_vol(bid, ticker.vol_usdt)
    if filt_ask.empty and filt_bid.empty:
        return 0
    elif filt_ask.empty:
        print(f'{ticker.get_name(ticker.ticker)}\n-----------------\n {filt_bid}\n\n')
    elif filt_bid.empty:
        print(f'{ticker.get_name(ticker.ticker)}\n{filt_ask}\n-----------------\n\n')
    else:
        print(f'{bidask(filt_ask, filt_bid, ticker.get_name(ticker.ticker))}\n\n')


def main():
    lim = input("Введите количество тикеров: ")
    vol = input("Введите объем для фильтра: ")
    all_tickers = get_all_tickers()
    tickers = []
    for i in all_tickers:
        tickers.append(Coin(i, lim, vol))
    # start = time()
    for i in tickers:
        th.Thread(target=vyzov, args=([i])).start()
    # print(f'Время работы: {time() - start}')


main()
