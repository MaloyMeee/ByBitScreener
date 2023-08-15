from pybit.unified_trading import WebSocket
from time import sleep
import threading as th
from config import api_key, api_secret
from pybit.unified_trading import HTTP
import pandas as pd
import dearpygui.dearpygui as dpg

pd.set_option('display.max_rows', None)

session = HTTP(api_key=api_key, api_secret=api_secret, testnet=False)  # создание сессии

ws = WebSocket(
    testnet=False,
    channel_type="linear",
)

global_all_tickers = []
volume_usdt = 0


def get_all_tickers():  # все тикеры фьючерсов
    global global_all_tickers
    all_tickers = []
    symbol = session.get_instruments_info(
        category="linear",
        status="Trading",
    )
    request = symbol.get('result').get('list')  # КАК-ТО УДАЛИТЬ ЕБУЧИЕ ОПЦИОНЫ
    for i in request:
        if '-' in i.get('symbol'):
            request.remove(i)
            continue
        else:
            all_tickers.append(i.get('symbol'))
            global_all_tickers.append(i.get('symbol'))
    return all_tickers


th.Thread(target=get_all_tickers).start()


def get_ask(message):
    ask = pd.DataFrame(message.get('data').get('a'),
                       columns=['price', 'volume'])  # делаем аск таблицу с ценой и объемом
    ask.price = ask.price.astype(float)
    ask.volume = ask.volume.astype(float)
    ask['vol_usdt'] = ask['price'] * ask['volume']  # добавляем столбец с объемом в баксах
    ask.vol_usdt = ask.vol_usdt.astype(int)
    ask.index += 1
    ask = ask.reindex(index=ask.index[::-1])  # переворачиваем таблицу по вертикали
    return ask


def get_bid(message):
    bid = pd.DataFrame(message.get('data').get('b'),
                       columns=['price', 'volume'])  # делаем бид таблицу с ценой и объемом
    bid.price = bid.price.astype(float)
    bid.volume = bid.volume.astype(float)
    bid['vol_usdt'] = bid['price'] * bid['volume']  # добавляем столбец с объемом в баксах
    bid.vol_usdt = bid.vol_usdt.astype(int)
    bid.index += 1
    return bid


def filter_usdt_vol(table, vol):
    filtered_vol = table[table['vol_usdt'] >= int(vol)]
    return filtered_vol


def get_name(message):
    ticker = message.get('data').get('s')
    return ticker


def get_tic(ticker):  # парсим и инфы о минимальной цене шага по тикеру
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


def bidask(ask, bid, ticker):
    zero = pd.DataFrame({'price': ['-----'], 'volume': ['-----'], 'vol_usdt': [ticker]})
    bidask = pd.concat([ask, zero])
    bidask = pd.concat([bidask, bid])
    return bidask


def handle_message(message):
    # print(message)
    ticker = get_name(message)
    ask = get_ask(message)
    bid = get_bid(message)
    filt_ask = filter_usdt_vol(ask, volume_usdt)
    filt_bid = filter_usdt_vol(bid, volume_usdt)
    if filt_ask.empty and filt_bid.empty:
        return 0
    elif filt_ask.empty:
        print('1')
        return ticker, filt_bid
    elif filt_bid.empty:
        print('2')
        return ticker, filt_ask
    else:
        print('3')
        askbid = bidask(filt_ask, filt_bid, ticker)
        return askbid


def websocket_thread(symbol):
    x = ws.orderbook_stream(
        depth=500,
        symbol=symbol,
        callback=handle_message
    )
    while True:
        sleep(0)


def main():
    global volume_usdt
    volume_usdt = input('Volume: ')
    all_tickers = get_all_tickers()
    for i in all_tickers:
        th.Thread(target=websocket_thread, args=(i,)).start()
    while True:
        if len(all_tickers) != len(global_all_tickers):
            list_difference = []
            for element in global_all_tickers:
                if element not in all_tickers:
                    list_difference.append(element)
            for i in list_difference:
                th.Thread(target=websocket_thread, args=(i,)).start()
            all_tickers = global_all_tickers


main()
