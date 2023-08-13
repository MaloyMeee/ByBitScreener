from config import api_key, api_secret
from pybit.unified_trading import HTTP
import pandas as pd

session = HTTP(api_key=api_key, api_secret=api_secret, testnet=False)  # создание сессии
#session = HTTP(testnet=True)

class Coin():
    def __init__(self, name, lim, vol):
        self.ticker = name
        self.limit = lim
        self.vol_usdt = vol

    def get_name(self, ticker):
        return ticker

    def get_tic(self, ticker):  # парсим и инфы о минимальной цене шага по тикеру
        tic = session.get_instruments_info(  # парсим инфу о тикерах
            category="linear",
            symbol=ticker
        )
        tic = tic.get('result')  # начало поиска минмиального шага цены
        tic = tic.get('list')
        tic = tic[0]
        tic = tic.get('priceFilter')
        tic = tic.get('tickSize')
        return tic

    def get_ask(self, ticker, limit):  # парсинг аск заявок по тикеру с указанным лимитом
        tiker = session.get_orderbook(  # запрос инфы в ордербуке
            category="linear",
            symbol=ticker,
            limit=limit,
            ts=0
        )
        ask = pd.DataFrame(tiker.get('result').get('a'), columns=['price', 'volume'])  # делаем аск таблицу с ценой и объемом
        ask.price = ask.price.astype(float)
        ask.volume = ask.volume.astype(float)
        ask['vol_usdt'] = ask['price'] * ask['volume'] # добавляем столбец с объемом в баксах
        ask.vol_usdt = ask.vol_usdt.astype(int)
        ask.index += 1
        ask = ask.reindex(index=ask.index[::-1])  # переворачиваем таблицу по вертикали
        return ask

    def get_bid(self, ticker, limit):  # парсинг бид заявок по тикеру с указанным лимитом
        tiker = session.get_orderbook(  # запрос инфы в ордербуке
            category="linear",
            symbol=ticker,
            limit=limit,
            ts=0
        )
        bid = pd.DataFrame(tiker.get('result').get('b'), columns=['price', 'volume'])  # делаем бид таблицу с ценой и объемом
        bid.price = bid.price.astype(float)
        bid.volume = bid.volume.astype(float)
        bid['vol_usdt'] = bid['price'] * bid['volume'] # добавляем столбец с объемом в баксах
        bid.vol_usdt = bid.vol_usdt.astype(int)
        bid.index += 1
        return bid

    def filter_usdt_vol(self, table, vol):
        filtered_vol = table[table['vol_usdt'] >= int(vol)]
        return filtered_vol
