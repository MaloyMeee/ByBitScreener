import flet as ft

def main(page: ft.Page):
    page.title = "Screener Volume"
    page.version = ft.MainAxisAlignment.CENTER

ft.app(target=main, view=ft.WEB_BROWSER)