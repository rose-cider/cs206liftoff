import flet as ft
from home_app import render_home
from today_workout_page import render_workout

def main(page: ft.Page):

    def route_change(e):
        if page.route == "/workout":
            render_workout(page)
        else:
            render_home(page)

    # Set up route handling
    page.on_route_change = route_change
    page.go(page.route or "/")

ft.app(target=main, assets_dir="assets")
