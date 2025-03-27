import flet as ft
from groq import Groq
from config.api_config import GROQ_API_KEY

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize conversation history as a global variable
global conversation_history
conversation_history = [
    {"role": "system", "content": "You are a silly and sweet hamster named Hammer that's also a fitness trainer, and have been assigned as a coach for the fitness app LiftOff. LiftOff is designed to automatically adjust workouts to fit people's busy schedules, while allowing them to still reach their goals.Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences, and feel free to break each message into smaller ones that are sent together for a more real-human type feel. Ask for the user's name and call them by that, and also remember to ask for their height, current fitness level, times they'd like to exercise a week (and how long each session), as well as if they have access to a gym. Then provide a detailed workout regimen for one week, how many months it'll take to reach their goal, and ask if they're ok with it or need adjustments."}
]

def main(page: ft.Page):
    page.title = "AI Chat App"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True

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
                    bgcolor=ft.colors.ORANGE_500,
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
                    content=ft.Text("Squeak! Welcome! I'm Hammer, your AI fitness trainer. How can I help you today?", color=ft.colors.WHITE, no_wrap=False),
                    bgcolor=ft.colors.ORANGE_500,
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

ft.app(target=main)
