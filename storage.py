#ФАЙЛ - ХРАНИЛИЩЕ ДЛЯ ФУНКЦИЙ, ЕСЛИ ВДРУГ НАДО БУДЕТ ВЕРНУТЬ


# TODO сделать ретерн таблицы
def get_ask(message):
    ask = message.get('data').get('a')
    with dpg.window(label='ask'):
        with dpg.table(header_row=True):
            dpg.add_table_column(label='price')
            dpg.add_table_column(label='volume')
            dpg.add_table_column(label='vol_usdt')
            for i in ask:
                with dpg.table_row():
                    for j in range(0, 2):
                        dpg.add_text(i[j])
                    for k in range(0, 1):
                        dpg.add_text(str(int(float(i[0]) * float(i[1]))))
        return dpg.table(label='ask')


# TODO сделать ретерн таблицы
def get_bid(message):
    bid = message.get('data').get('b')
    with dpg.window(label='bid'):
        with dpg.table(header_row=True, ):
            dpg.add_table_column(label='price')
            dpg.add_table_column(label='volume')
            dpg.add_table_column(label='vol_usdt')
            for i in bid:
                with dpg.table_row():
                    for j in range(0, 2):
                        dpg.add_text(i[j])
                    for k in range(0, 1):
                        dpg.add_text(str(int(float(i[0]) * float(i[1]))))


# TODO сделать фулл функцию, которая будет флильтровать таблицу по объему
def filter_usdt_vol(table, volume_usdt):
    with dpg.window(label='filt'):
        with dpg.table(header_row=True, ):
            dpg.add_table_column(label='price')
            dpg.add_table_column(label='volume')
            dpg.add_table_column(label='vol_usdt')
            for i in table:
                with dpg.table_row():
                    if float(i[0]) * float(i[1]) < volume_usdt:
                        continue
                    else:
                        for j in range(0, 2):
                            dpg.add_text(i[j])
                        for k in range(0, 1):
                            dpg.add_text(str(int(float(i[0]) * float(i[1]))))
    pass

def get_name(message):
    ticker = message.get('data').get('s')
    return ticker

# TODO сделать фулл функцуию, которая будет объединять таблицу бидов и асков и называет окно названием тикера
def bidask(ask, bid, ticker):
    pass

# TODO доделать вторую половину функции
def handle_message(message):
    print(message)
    ticker = get_name(message)
    print(ticker)
    ask = get_ask(message)
    bid = get_bid(message)
    print(ask)
    print('after ask')
    volume_usdt = dpg.get_value('volume_in_usdt')  # ВСЕ ЧТО НИЖЕ - НЕ РАБОТАЕТ
    filt_ask = filter_usdt_vol(ask, volume_usdt)
    filt_bid = filter_usdt_vol(bid, volume_usdt)
    if filt_ask.empty and filt_bid.empty:
        return 0
    elif filt_ask.empty:
        return ticker, filt_bid
    elif filt_bid.empty:
        return ticker, filt_ask
    else:
        askbid = bidask(filt_ask, filt_bid, ticker)
        return askbid