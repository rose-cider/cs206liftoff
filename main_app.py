# main_app.py
import flet as ft
from chat_app import main as chat_main
from personality_quiz import PersonalityQuiz

def main(page: ft.Page):
    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True

    def launch_chat(e):
        page.clean()
        chat_main(page)
        
    def launch_quiz(e):
        page.clean()
        PersonalityQuiz().main(page)

    home_view = ft.Column(
        [
            ft.ElevatedButton("AI Buddy", on_click=launch_chat),
            ft.ElevatedButton("Personality Quiz", on_click=launch_quiz)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )
    
    page.add(home_view)

ft.app(target=main)
