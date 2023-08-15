import dearpygui.dearpygui as dpg
import pandas as pd
import dearpygui.demo as demo
import wsoctry as wsctry

dpg.create_context()
dpg.create_viewport(title="Screener", width=800, height=600)

demo.show_demo()

with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        pass

    with dpg.menu(label="Settings"):
        pass

    with dpg.menu(label="Help"):
        pass

with dpg.window(tag="Main", label='Volume in USDT', width=800, height=200):
    with dpg.menu_bar():
        with dpg.menu(label="Tocken"):
            # for i in wsctry.get_all_tickers():
            #     dpg.add_checkbox(label=i)
            pass

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
