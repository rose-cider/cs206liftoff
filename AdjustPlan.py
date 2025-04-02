import flet as ft
import os
import csv
from groq import Groq
from config.api_config import GROQ_API_KEY
import datetime
from header_utils import create_header

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Global conversation history
global conversation_history
conversation_history = []

# Load workout data from the reference file (LiftOff_Ref_Data.txt)
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

# Function to load adjusted workout plan
def load_adjusted_plan():
    file_path = os.path.join(os.getcwd(), "userdata", "adjusted.csv")
    adjusted_plan = []
    
    if not os.path.exists(file_path):
        return adjusted_plan
    
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                adjusted_plan.append(row)
    except Exception as e:
        print(f"Error loading adjusted plan: {str(e)}")
    
    return adjusted_plan

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

# Function to display adjusted workout plan
def show_adjusted_workout_plan(e):
    

    # Placeholder text to simulate interaction with AI
    user_filler_text = "This workout plan is way too rigorous. Two days at most, plz? No more than 1.5h"
    chat.controls.append(ft.Row([ft.Container(
        content=ft.Markdown(f"{user_filler_text}"),
        bgcolor=ft.colors.BLUE_GREY_100,
        padding=10,
        border_radius=10,
        width=window_width * 0.7,
    )], alignment=ft.MainAxisAlignment.END))

    chat.update()

    chat.controls.append(ft.Row([ft.Container(
        content=ft.Markdown("I'm thinking about how to adjust your workout...\n(Please wait, I am adjusting your plan!)"),
        bgcolor=ft.colors.ORANGE_400,
        padding=10,
        border_radius=10,
        width=window_width * 0.7,
    )], alignment=ft.MainAxisAlignment.START))
    
    chat.update()
    # Wait a moment before returning the adjusted plan
    adjusted_plan = load_adjusted_plan()
    
    if not adjusted_plan:
        chat.controls.append(ft.Row([ft.Container(
            content=ft.Markdown("No adjusted workout plan available."),
            bgcolor=ft.colors.RED_100,
            padding=10,
            border_radius=10,
            width=window_width * 0.7,
        )], alignment=ft.MainAxisAlignment.START))
    else:
        plan_text = "### Adjusted Workout Plan:\n"
        grouped_workouts = {}
        for workout in adjusted_plan:
            day = int(workout['day']) + 1  # Convert day from 0-indexed to 1-indexed
            if day not in grouped_workouts:
                grouped_workouts[day] = []
            grouped_workouts[day].append(workout)
        
        for day, workouts in grouped_workouts.items():
            plan_text += f"\n**Day {day}**:\n"
            for workout in workouts:
                workout_description = workout_data.get(workout['workout_code'], {}).get("description", "Description not found")
                plan_text += f"- {workout_description}: {workout['total_time_needed']}\n"
        
        chat.controls.append(ft.Row([ft.Container(
            content=ft.Markdown(plan_text),
            bgcolor=ft.colors.GREEN_100,
            padding=10,
            border_radius=10,
            width=window_width * 0.7,
        )], alignment=ft.MainAxisAlignment.START))
    
    chat.update()

# Function to display current workout plan
def show_current_workout_plan(e):
    weekly_plan = load_weekly_plan()
    
    if not weekly_plan:
        chat.controls.append(ft.Row([ft.Container(
            content=ft.Markdown("No current workout plan available."),
            bgcolor=ft.colors.RED_100,
            padding=10,
            border_radius=10,
            width=window_width * 0.7,
        )], alignment=ft.MainAxisAlignment.START))
        chat.update()
        return
    
    plan_text = "### Current Workout Plan:\n"
    grouped_workouts = {}
    for workout in weekly_plan:
        day = int(workout['day']) + 1  # Convert day from 0-indexed to 1-indexed
        if day not in grouped_workouts:
            grouped_workouts[day] = []
        grouped_workouts[day].append(workout)
    
    for day, workouts in grouped_workouts.items():
        plan_text += f"\n**Day {day}**:\n"
        for workout in workouts:
            workout_code = workout['workout_code']
            workout_description = workout_data.get(workout_code, {}).get("description", "Description not found")
            plan_text += f"- {workout_description}: {workout['total_time_needed']}\n"
    
    chat.controls.append(ft.Row([ft.Container(
        content=ft.Markdown(plan_text),
        bgcolor=ft.colors.YELLOW_100,
        padding=10,
        border_radius=10,
        width=window_width * 0.7,
    )], alignment=ft.MainAxisAlignment.START))
    
    chat.update()

# Main UI function
def render_change_plans(page: ft.Page):
    global chat
    global window_width
    
    page.title = "Adjust Workout Plan"
    page.window_width = 390
    page.window_height = 844
    window_width = page.window_width  # Save window width for other parts

    header = create_header("Adjust Workout Plan", True, lambda e: page.go("/"), False)

    chat = ft.Column(
        scroll="auto",
        expand=True,
        controls=[ft.Row([ft.Container(
            content=ft.Markdown("Hey! Heard you needed some help with adjusting your workout?"),
            bgcolor=ft.colors.ORANGE_400,
            padding=10,
            border_radius=10,
            width=page.window_width * 0.7,
        )], alignment=ft.MainAxisAlignment.START)]
    )
    
    adjust_button = ft.ElevatedButton("Adjust Workout Plan", on_click=show_adjusted_workout_plan)
    current_plan_button = ft.ElevatedButton("Show Current Workout Plan", on_click=show_current_workout_plan)
    
    # window.add(ft.Column([chat, ft.Row([adjust_button, current_plan_button], alignment=ft.MainAxisAlignment.CENTER)], expand=True))
    page.views.append(ft.View("/chat", [header, chat, ft.Row([adjust_button, current_plan_button])]))
    page.update()

# ft.app(target=render_change_plans)
