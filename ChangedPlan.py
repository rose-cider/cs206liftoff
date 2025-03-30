import flet as ft
import os
import csv
from groq import Groq
from config.api_config import GROQ_API_KEY
import datetime

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Global conversation history
global conversation_history
conversation_history = []

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

# Function to generate a weekly workout plan based on user preferences
def generate_weekly_plan(workout_days, session_duration, gym_access):
    weekly_plan = []
    available_workouts = {code: details for code, details in workout_data.items() if (gym_access or details["category"] != "Gym")}
    
    day_index = 0
    for _ in range(workout_days):
        day_workouts = []
        total_time = 0
        
        # Select workouts until session duration is filled
        for code, details in available_workouts.items():
            estimated_time_per_set = int(details["description"].split("(")[1].split()[0])  # Extract time/reps from description
            
            if total_time + estimated_time_per_set <= session_duration:
                day_workouts.append({
                    "day": day_index,
                    "workout_code": code,
                    "estimated_time_per_set": f"{estimated_time_per_set} min",
                    "total_time_needed": f"{estimated_time_per_set * 2} min",  # Assuming 2 sets per workout
                    "completed": "No"
                })
                total_time += estimated_time_per_set * 2
        
        weekly_plan.extend(day_workouts)
        day_index += 1
    
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

# Function to load weekly workout plan
def load_weekly_plan():
    file_path = os.path.join(os.getcwd(), "userdata", "weekly.csv")
    weekly_plan = []
    
    if not os.path.exists(file_path):
        return weekly_plan
    
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                weekly_plan.append(row)
    except Exception as e:
        print(f"Error loading weekly plan: {str(e)}")
    
    return weekly_plan

# Main function with personality integration
def main(page: ft.Page, personality="Athena"):
    global conversation_history
    global workout_data  # Access the workout_data

    page.title = f"Testing {personality}'s Response"
    page.window_width = 390
    page.window_height = 844

    # Personality configuration
    personalities_config = {
        "Athena": {
            "greeting": f"Hoot! I'm Athena, your wise and serious owl coach. Let's crush your goals together!",
            "icon": "assets/athena_icon.png",
            "system_message": (
                f"You are Athena, a direct and motivating strict owl fitness coach. "
                f"Provide structured and actionable advice in a professional tone."
            )
        },
        "Hammer": {
            "greeting": f"Squeak! I'm Hammer, your silly hamster buddy! Let's chat about your goals!",
            "icon": "assets/hammer_icon.png",
            "system_message": (
                f"You are Hammer, a silly collaborative and supportive hamster fitness coach. "
                f"Provide helpful advice in a friendly tone."
            )
        },
        "Felix": {
            "greeting": f"Chirp! I'm Felix, your cheerful gym buddy! Ready to have some fun while we work on your fitness?",
            "icon": "assets/felix_icon.png",
            "system_message": (
                f"You are Felix, a friendly cheerful and motivational bird fitness coach. "
                f"Motivate the user with positivity and let them take charge of their journey."
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
            
            # Parse user preferences and generate a workout plan if prompted
            if user_input.lower().startswith("generate plan"):
                preferences = user_input.split(":")[1].strip().split(",")
                workout_days = int(preferences[0])
                session_duration = int(preferences[1])
                gym_access = preferences[2].strip().lower() == "yes"
                
                weekly_plan = generate_weekly_plan(workout_days, session_duration, gym_access)
                save_weekly_plan(weekly_plan)
                
                ai_response += "\n\n✅ Weekly workout plan generated and saved!"
            
            conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}"

    def send_message(user_input):
        chat.controls.append(ft.Row([
            ft.Container(
                content=ft.Markdown(user_input),
                bgcolor=ft.colors.BLUE_GREY_100,
                padding=10,
                border_radius=10,
                width=page.window_width * 0.7,
            )
        ], alignment=ft.MainAxisAlignment.END))

        ai_response = chat_with_ai(user_input)
        chat.controls.append(ft.Row([
            ft.Container(
                content=ft.Markdown(ai_response),
                bgcolor=ft.colors.ORANGE_500,
                padding=10,
                border_radius=10,
                width=page.window_width * 0.7,
            )
        ], alignment=ft.MainAxisAlignment.START))

        page.update()

    def send_test_query(e):
        user_input = "I'm not sure I want to workout today..."
        send_message(user_input)

    def show_current_workout_plan(e):
        weekly_plan = load_weekly_plan()
        
        if not weekly_plan:
            send_message("No workout plan available. Generate one first!")
            return
        
        grouped_workouts = {}
        for workout in weekly_plan:
            day = int(workout['day']) + 1
            if day not in grouped_workouts:
                grouped_workouts[day] = []
            grouped_workouts[day].append(workout)

        plan_text = "### Current Workout Plan:\n"
        for day, workouts in grouped_workouts.items():
            plan_text += f"\n**Day {day}**:\n"
            for workout in workouts:
                workout_code = workout['workout_code']
                workout_description = workout_data.get(workout_code, {}).get("description", "Description not found")
                plan_text += f"- {workout_description} - {workout['estimated_time_per_set']} (Total: {workout['total_time_needed']})\n"
        
        chat.controls.append(ft.Row([
            ft.Container(
                content=ft.Markdown(plan_text),
                bgcolor=ft.colors.GREEN_100,
                padding=10,
                border_radius=10,
                width=page.window_width * 0.7,
            )
        ], alignment=ft.MainAxisAlignment.START))
        
        page.update()

    chat = ft.Column(
        scroll="auto",
        expand=True,
        controls=[
            ft.Row([
                ft.Container(
                    content=ft.Markdown(config["greeting"]),
                    bgcolor=ft.colors.ORANGE_400,
                    padding=10,
                    border_radius=10,
                    width=page.window_width * 0.7,
                )
            ], alignment=ft.MainAxisAlignment.START)
        ]
    )

    test_button = ft.ElevatedButton("Test AI Response", on_click=send_test_query)
    current_plan_button = ft.ElevatedButton("Current Workout Plan", on_click=show_current_workout_plan)

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
                ft.Row([test_button, current_plan_button]),
            ],
            expand=True,
        )
    )

# To test different AI responses, simply uncomment the one you'd like to test out.
# ft.app(target=lambda p: main(p, personality="Athena"))
# ft.app(target=lambda p: main(p, personality="Felix")) 
ft.app(target=lambda p: main(p, personality="Hammer"))
