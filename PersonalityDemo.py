import flet as ft
from groq import Groq
from nav_utils import create_navbar
from config.api_config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

# Abby's user profile data
user_profile = {
    "Name": "Abby",
    "Workout Frequency": "3 days",
    "Workout Types": ["Strength", "HIIT"],
    "Fitness Level": "Intermediate",
    "Duration (mins)": 45,
    "Location": "Home",
    "Height (cm)": 100,
    "Current Weight (kg)": 20,
    "Goal": "Build Muscle",
    "Target Weight (kg)": None,
    "Goal Duration (months)": 7,
}

# Global conversation history
global conversation_history
conversation_history = []

def main(page: ft.Page, personality="Athena"):
    global conversation_history
    
    page.title = f"Testing {personality}'s Response"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True
    
    # Personality configuration
    personalities_config = {
        "Athena": {
            "greeting": f"Hoot! I'm Athena, your wise and serious owl coach. Let's crush your goals together!",
            "icon": "assets/athena_icon.png",
            "system_message": (
                f"You are Athena, a direct and motivating strict owl fitness coach. Provide real human workouts and with specific instructions on how to do them, and how many reps or how long. "
                f"Provide structured and actionable advice in a professional tone. "
                f"User profile: {user_profile}. Respond to the user asking to change her workout plan."
            )
        },
        "Hammer": {
            "greeting": f"Squeak! I'm Hammer, your silly hamster buddy! Let's chat about your goals!",
            "icon": "assets/hammer_icon.png",
            "system_message": (
                f"You are Hammer, a silly collaborative and supportive hamster fitness coach. Provide real human workouts and with specific instructions on how to do them, and how many reps or how long. "
                f"Provide helpful advice in a friendly tone. "
                f"User profile: {user_profile}. Respond to the user asking to change her workout plan."
            )
        },
        "Felix": {
            "greeting": f"Chirp! I'm Felix, your cheerful gym buddy! Ready to have some fun while we work on your fitness?",
            "icon": "assets/felix_icon.png",
            "system_message": (
                f"You are Felix, a friendly cheerful and motivational bird fitness coach. "
                f"Motivate the user with positivity and let them take charge of their journey. Provide real human workouts and with specific instructions on how to do them, and how many reps or how long. "
                f"User profile: {user_profile}. Respond to the user asking to change her workout plan."
            )
        }
    }

    config = personalities_config.get(personality, personalities_config["Athena"])

    # Initialize conversation history with system message if it's empty
    if not conversation_history:
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

    def send_test_query(e):
        user_input = f"I'm not sure I want to workout today..."
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

    test_button = ft.ElevatedButton("Test AI Response", on_click=send_test_query)

    bottom_nav = create_navbar(
        active="chat",
        on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src=config["icon"], width=40, height=40),
                        ft.Text(f"{personality}", size=24, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                chat,
                test_button,
                bottom_nav  # Add bottom navigation bar here
            ],
            expand=True,
        )
    )

# To test different AI responses, simply uncomment the one you'd like to test out.
ft.app(target=lambda p: main(p, personality="Athena"))
# ft.app(target=lambda p: main(p, personality="Felix"))
# ft.app(target=lambda p: main(p, personality="Hammer"))

# Then, run this:
# flet run PersonalityDemo.py