# chat_app.py
import flet as ft
from groq import Groq
from config.api_config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def main(page: ft.Page):
    # Set window size and shape to mimic an iPhone
    page.title = "AI Chat App"
    page.window_width = 390  # iPhone width
    page.window_height = 844  # iPhone height
    page.window_frameless = True  # Remove title bar

    def chat_with_ai(user_input):
        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[
                    {"role": "system", "content": "You are a silly and sweet hamster that's also a fitness trainer. Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences."},
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
                    bgcolor=ft.colors.BLUE_GREY_100,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.END))
            
            ai_response = chat_with_ai(user_input)
            chat.controls.append(ft.Row([
                ft.Container(
                    content=ft.Text(ai_response, color=ft.colors.WHITE, no_wrap=False),
                    bgcolor=ft.colors.PINK_300,
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
                    content=ft.Text("Squeak! Welcome! I'm your Hammer, your AI fitness trainer. How can I help you today?", color=ft.colors.WHITE, no_wrap=False),
                    bgcolor=ft.colors.PINK_300,
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
                        ft.Image(src="assets/hammer_icon.png", width=40, height=40),
                        ft.Text("AI Hamster Fitness Trainer", size=24, weight="bold"),
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
ft.app(target=main)
