import flet as ft
from home_app import render_home
from today_workout_page import render_workout
from goals import render_goals
from login import render_login
from personality_quiz import render_quiz

def main(page: ft.Page):

    def route_change(e):
        print("Route changed to:", page.route)
        if page.route == "/login":
            render_login(page)
        elif page.route == "/quiz":
            render_quiz(page)
        elif page.route == "/workout":
            render_workout(page)
        elif page.route == "/goals":  
            render_goals(page)
        else:
            render_home(page)

    # Set up route handling
    page.on_route_change = route_change
    page.go("/login")  # Start the app on the login page

ft.app(target=main, assets_dir="assets")