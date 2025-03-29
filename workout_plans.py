import flet as ft
import os
import csv
from shared_data import user_inputs

user_name = ft.TextField(
    label="Your Name",
    label_style=ft.TextStyle(color=ft.colors.BLACK),
    width=300,
    color=ft.colors.BLACK
)

def user_name_step(back_step, next_step):
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                        ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    padding=ft.padding.only(top=200),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Welcome!", size=25, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK),
                            ft.Text("What's your name?", size=18, text_align="center", color=ft.colors.BLACK),
                            user_name
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    padding=ft.padding.only(top=150),
                    content=ft.ElevatedButton(
                        "Continue",
                        on_click=lambda e: (user_inputs.update({"name": user_name.value}), next_step(e)),
                        width=250,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=12)
                        )
                    )
                )
            ],
            spacing=25,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def workout_frequency_step(back_step, next_step):

    frequency_dropdown = ft.Dropdown(
                                options=[ft.dropdown.Option(f"{i} days") for i in range(1, 8)],
                                value="3 days",
                                width=300,
                                color=ft.colors.BLACK
                            )
    
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                        ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    padding=ft.padding.only(top=200),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Tell us about your current\nworkout plans", size=18, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK),
                            ft.Text("How many times a week do you work out?", size=14, text_align="center", color=ft.colors.BLACK),
                            frequency_dropdown
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    padding=ft.padding.only(top=150),
                    content=ft.ElevatedButton("Continue", on_click=lambda e: (user_inputs.update({"frequency": frequency_dropdown.value}), next_step(e)), width=250,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=12)
                        ))
                )
            ],
            spacing=25,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def workout_types_step(back_step, next_step):
    chips = []
    selected = user_inputs["types"]

    def toggle_chip(e):
        chip = e.control
        label = chip.text
        if label in selected:
            selected.remove(label)
            chip.style = ft.ButtonStyle(
                bgcolor=ft.colors.WHITE,
                color=ft.colors.BLACK,
                side=ft.BorderSide(1, ft.colors.BLACK),
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=15, vertical=5)
            )
        else:
            selected.add(label)
            chip.style = ft.ButtonStyle(
                bgcolor=ft.colors.ORANGE,
                color=ft.colors.WHITE,
                side=ft.BorderSide(1, ft.colors.ORANGE),
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=15, vertical=5)
            )
        chip.update()


    for et in ["Strength", "Cardio", "Sports", "Pilates", "Yoga", "HIIT", "Aerobics", "Cycling", "Running", "Swimming", "Dance", "Endurance"]:
        chips.append(ft.TextButton(
            text=et,
            on_click=toggle_chip,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.WHITE,
                color=ft.colors.BLACK,
                side=ft.BorderSide(1, ft.colors.BLACK),
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=15, vertical=5)
            )
        ))


    return ft.Container(
    padding=ft.padding.symmetric(horizontal=20, vertical=30),
    content=ft.Column(
        controls=[
            # Header stays at the top
            ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                    ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            ft.Container(
                padding=ft.padding.only(top=150),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Tell us about your current\nworkout plans",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align="center",
                            color=ft.colors.BLACK
                        ),
                        ft.Text(
                            "What type of exercises are included in your plans?",
                            size=14,
                            text_align="center",
                            color=ft.colors.BLACK
                        ),
                        ft.Row(
                            controls=chips,
                            wrap=True,
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=100),
                            content=ft.ElevatedButton(
                                "Continue",
                                on_click=next_step,
                                width=250,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.ORANGE,
                                    color=ft.colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                    shape=ft.RoundedRectangleBorder(radius=12)
                                )
                            )
                        )
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ],
        spacing=25,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
)

def fitness_level_step(back_step, next_step):
    fitness_levels = ["Beginner", "Intermediate", "Advanced"]
    selected = {"value": user_inputs["level"] or "Beginner"}
    level_buttons = []

    default_style = ft.ButtonStyle(
        bgcolor=ft.colors.WHITE,
        color=ft.colors.BLACK,
        side=ft.BorderSide(1, ft.colors.BLACK),
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=10)
    )

    selected_style = ft.ButtonStyle(
        bgcolor=ft.colors.ORANGE,
        color=ft.colors.WHITE,
        side=ft.BorderSide(1, ft.colors.ORANGE),
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=10)
    )

    def select_level(e):
        selected["value"] = e.control.text
        user_inputs["level"] = selected["value"]
        for btn in level_buttons:
            btn.style = selected_style if btn.text == selected["value"] else default_style
            btn.update()

    for level in fitness_levels:
        btn = ft.TextButton(
            text=level,
            on_click=select_level,
            style=selected_style if level == selected["value"] else default_style,
            width=200
        )
        level_buttons.append(btn)

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                    ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    padding=ft.padding.only(top=150),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Tell us about your current\nworkout plans", size=18, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK),
                            ft.Text("What is your current fitness level?", size=14, text_align="center", color=ft.colors.BLACK),
                            ft.Column(controls=level_buttons, spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    padding=ft.padding.only(top=100),
                    content=ft.ElevatedButton("Continue", on_click=next_step, width=250,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=12)
                        ))
                )
            ],
            spacing=25,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def workout_duration_step(back_step, next_step):
    duration_field = ft.TextField(label="Duration (minutes)", value="65", width=200, color=ft.colors.BLACK)

    def sync_slider(e):
        duration_field.value = str(int(e.control.value))
        duration_field.update()

    slider = ft.Slider(min=30, max=120, divisions=18, value=65, label="{value} mins", on_change=sync_slider)

    return ft.Container(
    padding=ft.padding.symmetric(horizontal=20, vertical=30),
    content=ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                    ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            ft.Container(
                padding=ft.padding.only(top=150),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Tell us about your current\nworkout plans",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align="center",
                            color=ft.colors.BLACK
                        ),
                        ft.Text(
                            "How long do your workouts typically last?",
                            size=14,
                            text_align="center",
                            color=ft.colors.BLACK
                        ),
                        duration_field,
                        slider,
                        ft.Container(
                            padding=ft.padding.only(top=100),
                            content=ft.ElevatedButton(
                                "Continue",
                                on_click=lambda e: (user_inputs.update({"duration": duration_field.value}), next_step(e)),
                                width=250,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.ORANGE,
                                    color=ft.colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                    shape=ft.RoundedRectangleBorder(radius=12)
                                )
                            )
                        )
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ],
        spacing=25,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
)

def workout_location_step(back_step, next_step):

    location_dropdown = ft.Dropdown(
                                label="Location",
                                options=[
                                    ft.dropdown.Option("Gym"),
                                    ft.dropdown.Option("Home"),
                                    ft.dropdown.Option("Outdoors"),
                                    ft.dropdown.Option("Others")
                                ],
                                value="Gym",
                                width=250,
                                color=ft.colors.BLACK
                            )
    
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                    ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    padding=ft.padding.only(top=150),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Tell us about your current\nworkout plans", size=18, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK),
                            ft.Text("Where do you typically workout?", size=14, text_align="center", color=ft.colors.BLACK),
                            location_dropdown
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    padding=ft.padding.only(top=100),
                    content=ft.ElevatedButton("Finish!", 
                                              on_click=lambda e: (
                                                user_inputs.update({"location": location_dropdown.value}),
                                                next_step(e)
                                            ), width=250,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=12)
                        ))
                )
            ],
            spacing=25,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def workout_complete_step(back_step, next_step):
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                        ft.Text("Workout Plan", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.Container(width=40)  # spacer for alignment
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Container(
                    padding=ft.padding.only(top=250),
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Awesome!", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK, text_align="center"),
                            ft.Text("We'll tailor your workouts around your\nexisting workout plans!",
                                    size=14,
                                    color=ft.colors.GREY,
                                    text_align="center")
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),

                ft.Container(
                    padding=ft.padding.only(top=180),
                    content=ft.ElevatedButton(
                        text="Goal Planning",
                        on_click=next_step,
                        width=250,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=25)
                        )
                    )
                )
            ],
            spacing=25,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def main(page: ft.Page):
    page.title = "Workout Plan"
    page.window_width = 430
    page.window_height = 930
    page.window_resizable = False
    page.scroll = "auto"
    page.bgcolor = ft.colors.WHITE
    page.window_min_width = 430
    page.window_max_width = 430
    page.window_min_height = 930
    page.window_max_height = 930

    step_index = 0

    def back_step(e=None):
        nonlocal step_index
        if step_index > 0:
            step_index -= 1
            update_content()

    def next_step(e=None):
        nonlocal step_index
        if step_index < len(steps) - 1:
            step_index += 1
            update_content()
        else:
            import goal_setting  
            goal_setting.goal_setting_view(page)

    def update_content():
        phone_frame = ft.Container(
            content=steps[step_index](back_step, next_step),
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            alignment=ft.alignment.center
        )

        page.controls.clear()
        page.add(
            ft.Container(
                content=phone_frame,
                alignment=ft.alignment.center,
                expand=True
            )
        )

    steps = [
        user_name_step,
        workout_frequency_step,
        workout_types_step,
        fitness_level_step,
        workout_duration_step,
        workout_location_step,
        workout_complete_step
    ]

    update_content()

ft.app(target=main)