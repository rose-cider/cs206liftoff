# chat_app.py
import flet as ft
from groq import Groq
from config.api_config import GROQ_API_KEY
from personality_quiz import personality

client = Groq(api_key=GROQ_API_KEY)

def main(page: ft.Page):
    # Set window size and shape to mimic an iPhone
    page.title = "AI Chatbot"
    page.window_width = 390  # iPhone width
    page.window_height = 844  # iPhone height
    page.window_frameless = True  # Remove title bar

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

    # Get the configuration for the selected personality
    config = personalities_config.get(personality, personalities_config["Athena"])  # HI MIYA CHANGE THIS IF YOU WANT TO TRY THE OTHERS

    def chat_with_ai(user_input):
        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[
                    {"role": "system", "content": config["system_message"]},  # Use dynamic system message
                    {"role": "user", "content": user_input},
                ],
                max_tokens=500  # Allow longer responses
            )
            return response.choices[0].message.content
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
                    bgcolor=ft.Colors.PINK_300,
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
                    content=ft.Text(config["greeting"], color=ft.Colors.WHITE, no_wrap=False),  # Dynamic greeting
                    bgcolor=ft.Colors.PINK_300,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.START)
        ]
    )

    new_message = ft.TextField(hint_text="Type your message here...",
                                expand=True,
                                on_submit=send_message
    )
    send_button = ft.ElevatedButton("Send", on_click=send_message)

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src=config["icon"], width=40, height=40),  # Dynamic icon
                        ft.Text(f"AI {personality} Fitness Trainer", size=24, weight="bold"),  # Dynamic title
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
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
    )

# To run separately, uncomment:
# ft.app(target=main)