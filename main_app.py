# main_app.py
import flet as ft
from chat_app import main as chat_main
from personality_quiz import PersonalityQuiz

def main(page: ft.Page):
    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True

    quiz_instance = PersonalityQuiz()  # Instantiate PersonalityQuiz

    def launch_chat(page):
        page.clean()
        chat_main(page)

    def quiz_done_callback(personality):
        # Callback function to launch chat with selected personality
        page.clean()
        chat_main(page, personality=personality)

    def launch_quiz(e):
        page.clean()
        quiz_instance.main(page, quiz_done_callback=quiz_done_callback)  # Pass the callback

    home_view = ft.Column(
        [
            ft.ElevatedButton("AI Buddy", on_click=lambda e: launch_chat(page)),
            ft.ElevatedButton("Personality Quiz", on_click=launch_quiz)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    page.add(home_view)

ft.app(target=main)
