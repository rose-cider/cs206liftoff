import os
import csv

user_inputs = {
    "name": "",
    "frequency": "",
    "types": set(),
    "level": "",
    "duration": "",
    "location": "",
    "height": "",
    "current_weight": "",
    "goal": "",
    "target_weight": "",
    "goal_duration": ""
}

def save_to_csv():
    file_exists = os.path.isfile("userprofile.csv")

    with open("userprofile.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name", "Workout Frequency", "Workout Types", "Fitness Level", "Duration (mins)", "Location",
                "Height (cm)", "Current Weight (kg)", "Goal", "Target Weight (kg)", "Goal Duration (months)"
            ])

        writer.writerow([
            user_inputs["name"],
            user_inputs["frequency"],
            ", ".join(user_inputs["types"]),
            user_inputs["level"],
            user_inputs["duration"],
            user_inputs["location"],
            user_inputs["height"],
            user_inputs["current_weight"],
            user_inputs["goal"],
            user_inputs["target_weight"],
            user_inputs["goal_duration"]
        ])
