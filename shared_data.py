import os
import csv

# Define user inputs
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

# Ensure the 'userdata' folder exists
folder_path = "userdata"
if not os.path.exists(folder_path):
    print(f"The folder '{folder_path}' does not exist. Please create it before running the script.")
    exit()

# File path for the CSV file
csv_file_path = os.path.join(folder_path, "userprofile.csv")

def save_to_csv():
    # Check if the file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Open the CSV file in append mode
    with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header row if the file is being created for the first time
        if not file_exists:
            writer.writerow([
                "Name", "Workout Frequency", "Workout Types", "Fitness Level", "Duration (mins)", "Location",
                "Height (cm)", "Current Weight (kg)", "Goal", "Target Weight (kg)", "Goal Duration (months)"
            ])

        # Write user input data to the CSV file
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