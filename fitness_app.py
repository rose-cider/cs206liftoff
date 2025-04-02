import flet as ft
from home_app import render_home
from today_workout_page import render_workout
from goals import render_goals
from login import render_login
from personality_quiz import render_quiz
from goal_setting import goal_setting_view

def main(page: ft.Page):
    user_personality = "Felix"

    def on_quiz_done(personality):
        """Callback function to receive personality and proceed to goals."""
        nonlocal user_personality
        user_personality = personality  # Save personality choice
        print("Personality Result: ", personality)
        page.go("/goal-setting")

    def route_change(e):
        print("Route changed to:", page.route)
        if page.route == "/login":
            render_login(page)
        elif page.route == "/quiz":
            render_quiz(page, on_quiz_done)
        elif page.route == "/workout":
            render_workout(page)
        elif page.route == "/goals":  
            render_goals(page)
        elif page.route == "/goal-setting":
            goal_setting_view(page)
        else:
            render_home(page, chosen_character=user_personality)

    # Set up route handling
    page.on_route_change = route_change
    page.go("/login")  # Start the app on the login page

ft.app(target=main, assets_dir="assets")