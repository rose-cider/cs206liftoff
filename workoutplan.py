import flet as ft
import os
import csv
from groq import Groq
from config.api_config import GROQ_API_KEY
import datetime

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize conversation history
global conversation_history
conversation_history = [
    {"role": "system", "content": "You are a silly and sweet hamster named Hammer that's also a fitness trainer, and have been assigned as a coach for the fitness app LiftOff. LiftOff is designed to automatically adjust workouts to fit people's busy schedules, while allowing them to still reach their goals. Give realistic HUMAN exercises and fitness regimes though. Keep your responses short and concise. Break your answers into multiple short messages, each no longer than 2-3 sentences, and feel free to break each message into smaller ones that are sent together for a more real-human type feel. Ask for the user's name and call them by that, and also remember to ask for their height, current fitness level, times they'd like to exercise a week (and how long each session), as well as if they have access to a gym. Then provide a detailed workout regimen for one week, how many months it'll take to reach their goal, and ask if they're ok with it or need adjustments. Also write out roughly when the user will be done with reaching their goal, and how long it'll take at the current rate."}
]

# Function to load workout data from LiftOff_Ref_Data.txt
def load_workout_data():
    file_path = os.path.join(os.getcwd(), "assets", "LiftOff_Ref_Data.txt")
    workouts = {}
    
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist!")
        return workouts
    
    try:
        with open(file_path, "r") as file:
            current_category = ""
            for line in file:
                line = line.strip()
                if line.endswith("Workouts"):
                    current_category = line[:-9]
                elif line and ":" in line:
                    code, description = line.split(":", 1)
                    code = code.strip()
                    description = description.strip()
                    workouts[code] = {"category": current_category, "description": description}
    except Exception as e:
        print(f"Error loading workout data: {str(e)}")
    
    return workouts

# Load workout data at startup
workout_data = load_workout_data()

# Function to load weekly workout plan
def load_weekly_plan():
    file_path = os.path.join(os.getcwd(), "userdata", "weekly.csv")
    weekly_plan = []
    
    if not os.path.exists(file_path):
        print(f"Warning: The file {file_path} does not exist. Creating a new one.")
        return weekly_plan
    
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                weekly_plan.append(row)
    except Exception as e:
        print(f"Error loading weekly plan: {str(e)}")
    
    return weekly_plan

# Function to save weekly workout plan
def save_weekly_plan(weekly_plan):
    file_path = os.path.join(os.getcwd(), "userdata", "weekly.csv")
    
    try:
        with open(file_path, "w", newline='') as file:
            fieldnames = ["day", "workout_code", "estimated_time_per_set", "total_time_needed", "completed"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for workout in weekly_plan:
                writer.writerow(workout)
    except Exception as e:
        print(f"Error saving weekly plan: {str(e)}")

# Function to get today's workout
def get_workout_plan(day):
    weekly_plan = load_weekly_plan()
    return [w for w in weekly_plan if int(w["day"]) == day]

def main(page: ft.Page):
    page.title = "Lift Off"
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
        if not user_input:
            return

        # Display user input
        chat.controls.append(ft.Row([ 
            ft.Container(
                content=ft.Markdown(f"{user_input}"),
                bgcolor=ft.colors.BLUE_GREY_100,
                padding=10,
                border_radius=10,
                width=page.window_width * 0.7
            )
        ], alignment=ft.MainAxisAlignment.END))

        # Handle special commands
        if user_input.lower() == "today's workout":
            today = datetime.datetime.today().weekday()
            workouts_today = get_workout_plan(today)

            if workouts_today:
                workout_response = "**🏋️ Today's Workout:**\n" + "\n".join(
                    [f"- **{workout_data[w['workout_code']]['description']}** - ⏳ {w['total_time_needed']}" for w in workouts_today]
                )
            else:
                workout_response = "No workouts scheduled for today. Enjoy your rest day! 🐹"

            chat.controls.append(ft.Row([
                ft.Container(
                    content=ft.Markdown(workout_response),
                    bgcolor=ft.colors.ORANGE_400,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.START))
        else:
            # Get AI response
            ai_response = chat_with_ai(user_input)

            # Display AI response
            chat.controls.append(ft.Row([
                ft.Container(
                    content=ft.Markdown(f"{ai_response}"),
                    bgcolor=ft.colors.ORANGE_400,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7
                )
            ], alignment=ft.MainAxisAlignment.START))

        new_message.value = ""
        page.update()

    chat = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    new_message = ft.TextField(
        hint_text="Type a message...",
        border=ft.InputBorder.OUTLINE,
        expand=True,
        on_submit=send_message
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        on_click=send_message,
        icon_color=ft.colors.BLUE_400
    )

    # Add welcome message when app starts
    chat = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    # Add welcome message as a static element
    welcome_message = "Wheeee! Welcome to LiftOff! 🎉 I'm your fitness coach Hammer! Let's get started - what's your name?"
    chat.controls.append(ft.Row([
        ft.Container(
            content=ft.Markdown(welcome_message),
            bgcolor=ft.colors.ORANGE_400,
            padding=10,
            border_radius=10,
            width=page.window_width * 0.7
        )
    ], alignment=ft.MainAxisAlignment.START))

    new_message = ft.TextField(
        hint_text="Type a message...",
        border=ft.InputBorder.OUTLINE,
        expand=True,
        on_submit=send_message
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        on_click=send_message,
        icon_color=ft.colors.BLUE_400
    )

    page.add(
        chat,
        ft.Row(
            [new_message, send_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

ft.app(target=main)
