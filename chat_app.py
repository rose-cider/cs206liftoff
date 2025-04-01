import flet as ft
from groq import Groq
from config.api_config import GROQ_API_KEY

from nav_utils import create_navbar  # Import the navbar utility

client = Groq(api_key=GROQ_API_KEY)

# Global conversation history
global conversation_history
conversation_history = []

def main(page: ft.Page, personality=None):
    global conversation_history

    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True

    # Enable scrolling on the page
    page.scroll = ft.ScrollMode.ADAPTIVE  # Or .ALWAYS

    personalities_config = {
        "Athena": {
            "greeting": "Hoot! I'm Athena, your wise and serious owl coach. Let's crush your goals together!",
            "icon": "assets/athena_icon.png",
            "system_message": "You are Athena, a direct and motivating strict owl and fitness coach. Provide structured and actionable advice in a professional tone. Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences."
        },
        "Hammer": {
            "greeting": "Squeak! I'm Hammer, your silly hamster buddy! Let's chat about your goals!",
            "icon": "assets/hammer_icon.png",
            "system_message": "You are Hammer, a silly collaborative and supportive hamster, and fitness coach. Engage in open discussions and provide helpful advice in a friendly tone. Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences."
        },
        "Felix": {
            "greeting": "Chirp! I'm Felix, your cheerful gym buddy! Ready to have some fun while we work on your fitness?",
            "icon": "assets/felix_icon.png",
            "system_message": "You are Felix, a friendly cheerful and motivational bird, and fitness coach. Stay upbeat and fun, motivating users with positivity and let them take charge of their journey. Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences."
        }
    }

    config = personalities_config.get(personality, personalities_config["Felix"])

    # Initialize conversation history with system message if it's empty
    global conversation_history
    conversation_history.append({"role": "system", "content": config["system_message"]})

    def chat_with_ai(user_input):
        global conversation_history
        conversation_history.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=conversation_history,
                max_tokens=500
            )
            ai_response = response.choices[0].message.content
            if not isinstance(ai_response, str):
                ai_response = str(ai_response)
            conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}"

    def send_message(e):
        user_input = new_message.value
        if user_input:
            chat.controls.append(ft.Row([
                ft.Container(
                    content=ft.Text(user_input, no_wrap=False),
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.END))

            ai_response = chat_with_ai(user_input)
            chat.controls.append(ft.Row([
                ft.Container(
                    content=ft.Text(ai_response, color=ft.Colors.WHITE, no_wrap=False),
                    bgcolor=ft.Colors.ORANGE_500,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.START))

            new_message.value = ""
            page.update()

    chat = ft.Column(
        scroll="auto",
        expand=True,
        controls=[
            ft.Row([
                ft.Container(
                    content=ft.Text(config["greeting"], color=ft.Colors.WHITE, no_wrap=False),
                    bgcolor=ft.Colors.ORANGE_500,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.START)
        ]
    )

    new_message = ft.TextField(hint_text="Type your message here...",
                                expand=True,
                                on_submit=send_message)

    send_button = ft.ElevatedButton("Send", on_click=send_message)

# Custom header row
    chat_header_row = ft.Row(
        controls=[
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go('/'),
                          icon_color=ft.colors.BLACK),
            ft.Row(  # Combine image and text in a Row
                [
                    ft.Image(src=config["icon"], width=40, height=40),
                    ft.Text(f"{personality}", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ],
                spacing=0,  # Remove space between image and text
                vertical_alignment=ft.CrossAxisAlignment.CENTER # Align items vertically
            ),
            ft.Container()  # Placeholder for alignment
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER # Align items vertically
    )

    chat_content = ft.Column(
        [
            chat_header_row,  # Add the custom header row
            chat,
            ft.Row(
                [
                    new_message,
                    send_button,
                ],
            ),
        ],
        expand=True,
    )

    phone_frame = ft.Container(
        content=chat_content,
        width=390,
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
        alignment=ft.alignment.center,
    )

    page.add(phone_frame)

# To run separately, uncomment:
# ft.app(target=main)
