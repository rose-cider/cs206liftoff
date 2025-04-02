import flet as ft
from home_app import render_home
from today_workout_page import render_workout
from goals import render_goals
from login import render_login
from personality_quiz import render_quiz
from goal_setting import goal_setting_view
from workout_plans import render_workout_plans
from chat_app import render_chat
from AdjustPlan import render_change_plans

def main(page: ft.Page):
    # Page configuration (matches both login and quiz styling)
    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True
    page.padding = 0
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Poppins")

    user_personality = "Felix" # Default as Felix

    # Quiz completion handler
    def on_quiz_done(personality):
        """Callback function to receive personality and proceed to goals."""
        nonlocal user_personality
        user_personality = personality  # Save personality choice
        print("Personality Result: ", personality)
        page.go("/goal-setting")

    # Route handling
    def route_change(e):
        page.views.clear()
        
        if page.route == "/login":
            render_login(page)
        elif page.route == "/quiz":
            render_quiz(page, on_quiz_done)
        elif page.route == "/goal-setting":
            # goal_setting_view(page) # Link to goal_setting_view?
            render_workout_plans(page)
        elif page.route == "/chat":
            render_chat(page, user_personality)
        elif page.route == "/change-plans":
            render_change_plans(page)
        elif page.route == "/workout":
            render_workout(page, chosen_character=user_personality)
        elif page.route == "/goals":  
            render_goals(page)
        else:
            render_home(page, chosen_character=user_personality)

    # Setup routing
    page.on_route_change = route_change
    page.go("/login")  # Start with login page

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")