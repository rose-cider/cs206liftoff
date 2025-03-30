# main_app.py
import flet as ft
from chat_app import main as chat_main
from personality_quiz import PersonalityQuiz

def main(page: ft.Page):
    # Page settings
    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True

    # Set custom fonts and theme
    page.fonts = {"Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap"}
    page.theme = ft.Theme(font_family="Poppins")

    quiz_instance = PersonalityQuiz()  # Instantiate PersonalityQuiz

    def launch_chat(page, personality=None):
        """Launch the chat app with an optional personality."""
        page.clean()
        chat_main(page, personality=personality)

    def quiz_done_callback(personality):
        """Callback function to launch chat with the selected personality."""
        page.clean()
        chat_main(page, personality=personality)

    def launch_quiz(e):
        """Launch the personality quiz."""
        page.clean()
        quiz_instance.main(page, quiz_done_callback=quiz_done_callback)

    # Large centered welcome text
    welcome_text = ft.Text(
        "Welcome to LiftOff.",
        size=36,
        weight=ft.FontWeight.BOLD,
        color="#1A1A1A",
        text_align=ft.TextAlign.CENTER,
    )

    # Buttons for navigation
    ai_button = ft.ElevatedButton(
        text="AI Buddy",
        on_click=lambda e: launch_chat(page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=20,
            bgcolor="#FFA726",
            color="#FFFFFF",
            overlay_color={"hovered": "#FFB74D"},
        ),
    )

    quiz_button = ft.ElevatedButton(
        text="Personality Quiz",
        on_click=launch_quiz,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=20,
            bgcolor="#29B6F6",
            color="#FFFFFF",
            overlay_color={"hovered": "#4FC3F7"},
        ),
    )

    # Layout for home view
    home_view = ft.Column(
        [
            welcome_text,
            ft.Container(height=40),  # Spacer between text and buttons
            ai_button,
            quiz_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # Add the home view to the page
    page.add(home_view)

# Run the app
ft.app(target=main, port=8550, view=ft.WEB_BROWSER)
