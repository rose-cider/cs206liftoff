# info_steps.py
import flet as ft

class InfoStep(ft.Column):
    def __init__(self, title, fields, on_continue, on_back=None):
        super().__init__()
        self.title = ft.Text(value=title, size=20, weight=ft.FontWeight.BOLD)
        self.fields = fields
        self.continue_button = ft.ElevatedButton(
            text="Continue",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
            on_click=on_continue
        )
        self.back_button = ft.ElevatedButton(
            text="Back",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
            on_click=on_back,
            visible=on_back is not None # Only visible if there's a back action
        )
        self.controls = [
            self.title,
            *self.fields,
            ft.Row([
                self.back_button,
                self.continue_button
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True
        self.visible = False

    def get_values(self):
      data = {}
      for field in self.fields:
          if hasattr(field, 'label') and hasattr(field, 'value'):
              data[field.label] = field.value
          elif isinstance(field, ft.Column): # fitness radio values have no label attribute
              for item in field.controls:
                if isinstance(item, ft.RadioGroup):
                  data["Fitness Level"] = item.value
          elif isinstance(field, ft.Column):
            for item in field.controls:
              if isinstance(item, ft.Text):
                continue # skip the label
              for box in item.controls:
                data[box.label] = box.value
      return data

def create_steps(on_submit, on_back): # On back was not used
    """Create multi-step form components."""
    workout_types = ft.Column([
        ft.Text("What type of exercises are included in your plans?", weight=ft.FontWeight.BOLD),
        ft.Column([
        ft.Checkbox(label="Strength"),
        ft.Checkbox(label="Cardio"),
        ft.Checkbox(label="Sports"),
        ft.Checkbox(label="Pilates"),
        ft.Checkbox(label="Yoga"),
        ft.Checkbox(label="HIIT"),
        ft.Checkbox(label="Aerobics"),
        ft.Checkbox(label="Cycling"),
        ft.Checkbox(label="Running"),
        ft.Checkbox(label="Swimming"),
        ft.Checkbox(label="Dance"),
        ft.Checkbox(label="Endurance")
            ])
    ])
    fitness_level = ft.Column([
        ft.Text("What is your current fitness level?", weight=ft.FontWeight.BOLD),
        ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="beginner", label="Beginner"),
                ft.Radio(value="intermediate", label="Intermediate"),
                ft.Radio(value="advanced", label="Advanced"),
            ]),
        )
    ])
    duration = ft.TextField(label="Duration")
    frequency = ft.TextField(label="Frequency")
    location = ft.Column([
        ft.Text("Where do you typically workout?", weight=ft.FontWeight.BOLD),
        ft.Dropdown(
            options=[
                ft.dropdown.Option("Gym"),
                ft.dropdown.Option("Home"),
                ft.dropdown.Option("Outdoors"),
                ft.dropdown.Option("Other"),
            ],
            label="Location"
        )
    ])

    name = ft.TextField(label="Name")
    height = ft.TextField(label="Height")
    weight = ft.TextField(label="Weight")
    goal = ft.TextField(label="Goal")
    
    # Create the steps
    step1 = InfoStep("Tell us about you!", [name, height, weight, goal], on_continue=None, on_back=None)
    step2 = InfoStep("Workout Types", [workout_types], on_continue=None, on_back=None)
    step3 = InfoStep("Fitness Level", [fitness_level], on_continue=None, on_back=None)
    step4 = InfoStep("Workout Duration", [duration], on_continue=None, on_back=None)
    step5 = InfoStep("Workout Frequency", [frequency], on_continue=None, on_back=None)
    step6 = InfoStep("Workout Location", [location], on_continue=on_submit, on_back=None)

    return [step1, step2, step3, step4, step5, step6]
