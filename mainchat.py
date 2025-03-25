import flet as ft

def main(page: ft.Page):
    page.title = "AI Fitness Trainer Chat"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    chat_history = ft.Column(
        scroll="auto",
        expand=True,
        controls=[
            ft.Text("AI Trainer: Welcome! I'm your AI fitness trainer. How can I help you today?", color=ft.colors.BLUE),
            ft.Text("You: Can you suggest a workout for me?"),
            ft.Text("AI Trainer: Sure! How about a 30-minute cardio session followed by some strength training?", color=ft.colors.BLUE),
            ft.Text("You: That sounds good. What about diet tips?"),
            ft.Text("AI Trainer: Great question! Focus on eating plenty of vegetables, lean proteins, and whole grains.", color=ft.colors.BLUE),
            ft.Text("You: Thanks for the advice!"),
            ft.Text("AI Trainer: You're welcome! Remember to stay hydrated and get enough rest too.", color=ft.colors.BLUE),
        ]
    )

    user_input = ft.TextField(hint_text="Type your message here...", expand=True)

    page.add(
        ft.Column(
            [
                ft.Text("AI Fitness Trainer", size=24, weight="bold"),
                chat_history,
                ft.Row(
                    [
                        user_input,
                        ft.ElevatedButton("Send"),
                    ],
                ),
            ],
            expand=True,
        )
    )

ft.app(main)
