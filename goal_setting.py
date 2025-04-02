import flet as ft
from shared_data import user_inputs, save_to_csv

def goal_setting_view(page: ft.Page):
    page.views.clear()
    page.title = "Fitness Goal Setting"
    page.window_width = 430
    page.window_height = 930
    page.window_resizable = False
    page.scroll = "auto"
    page.bgcolor = ft.colors.WHITE

    page.window_min_width = 430
    page.window_max_width = 430
    page.window_min_height = 930
    page.window_max_height = 930

    step = ft.Ref[int]()
    step.value = 1

    selected_goal = ft.Text("")
    height_field = ft.TextField(label="Height (cm)", label_style=ft.TextStyle(color=ft.colors.BLACK), width=300, color=ft.colors.BLACK)
    current_weight = ft.TextField(label="Current weight (kg)",label_style=ft.TextStyle(color=ft.colors.BLACK), width=300, color=ft.colors.BLACK)
    target_weight = ft.TextField(label="Target weight (kg)",label_style=ft.TextStyle(color=ft.colors.BLACK), width=300, color=ft.colors.BLACK)
    bmi_warning = ft.Text("", color=ft.colors.RED, text_align="center")

    selected_month_value = {"value": ""}

    def go_to_step():
        step_content = None
        if step.value == 1:
            step_content = bmi_check_step()
        elif step.value == 2:
            step_content = goal_step()
        elif step.value == 3:
            step_content = weight_step()
        elif step.value == 4:
            step_content = month_step()
        elif step.value == 5:
            step_content = complete_step()

        phone_frame = ft.Container(
            content=step_content,
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            alignment=ft.alignment.center
        )
        page.views.append(ft.View("/goal-setting", [phone_frame]))
        page.update()

    def back_step(e):
        if step.value > 1:
            step.value -= 1
            go_to_step()

    def next_step(e=None):
        if step.value == 2 and (selected_goal.value == "Others" or selected_goal.value == "Build Muscle" or selected_goal.value == "Improve Endurance"):
            step.value = 4  # Skip target weight step
        elif step.value < 5:
            step.value += 1
        go_to_step()

    def goal_step():
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=20),
            content=ft.Column(
                controls=[
                    # Header stays in place
                    ft.Stack(
                        controls=[
                            ft.Row(
                                [
                                    ft.Text(
                                        "Goal Setting",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLACK
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ]
                    ),

                    # ⬆️ Shifted main content up using top padding
                    ft.Container(
                        padding=ft.padding.only(top=120),  # adjust this value to shift up/down
                        alignment=ft.alignment.top_center,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "What is your main fitness goal?",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    text_align="center",
                                    color=ft.colors.BLACK
                                ),
                                ft.Dropdown(
                                    label="Goal",
                                    width=300,
                                    color=ft.colors.BLACK,
                                    options=[
                                        ft.dropdown.Option("Lose Weight"),
                                        ft.dropdown.Option("Build Muscle"),
                                        ft.dropdown.Option("Improve Endurance"),
                                        ft.dropdown.Option("Others"),
                                    ],
                                    on_change=lambda e: setattr(selected_goal, "value", e.control.value)
                                )
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),

                    # Continue button stays in place
                    ft.Container(
                        padding=ft.padding.only(top=300),
                        content=ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Continue",
                                    on_click=lambda e: (user_inputs.update({"goal": selected_goal.value}), next_step(e)),
                                    width=250,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.ORANGE,
                                        color=ft.colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                        shape=ft.RoundedRectangleBorder(radius=12)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    )

                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def bmi_check_step():
        def calculate_bmi(e):
            try:
                height_cm = float(height_field.value)
                weight_kg = float(current_weight.value)
                height_m = height_cm / 100
                bmi = weight_kg / (height_m ** 2)
                bmi_warning.value = f"Your current BMI is {bmi:.1f}."
            except:
                bmi_warning.value = "Please enter valid numbers."
            page.update()
        
        def next_bmi_step(e):
            user_inputs["height"] = height_field.value
            user_inputs["current_weight"] = current_weight.value
            next_step(e)

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
            content=ft.Column(
                controls=[
                    # Header row
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                            ft.Text("Goal Setting", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                            ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    # Content centered
                    ft.Container(
                        padding=ft.padding.only(top=150),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Text("Let's check your BMI!", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK, text_align="center"),
                                ft.Container(content=height_field, alignment=ft.alignment.center),
                                ft.Container(content=current_weight, alignment=ft.alignment.center),
                                ft.ElevatedButton(
                                    text="Calculate BMI",
                                    on_click=calculate_bmi,
                                    width=250,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.ORANGE,
                                        color=ft.colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                        shape=ft.RoundedRectangleBorder(radius=12)
                                    )
                                ),
                                bmi_warning
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),

                    # Next button near the bottom
                    ft.Container(
                        padding=ft.padding.only(top=150),
                        content=ft.ElevatedButton(
                            text="Next",
                            on_click=next_bmi_step,
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

    def weight_step():
        def check_target_bmi(e):
            try:
                height_cm = float(height_field.value)
                weight_kg = float(target_weight.value)
                height_m = height_cm / 100
                bmi = weight_kg / (height_m ** 2)

                min_weight = 18.5 * (height_m ** 2)
                max_weight = 24.9 * (height_m ** 2)

                if bmi < 18.5 or bmi >= 25:
                    bmi_warning.value = (
                        f"⚠️ Warning: Your target BMI is {bmi:.1f}, which is considered unhealthy.\n\n"
                        f"For your height, a healthy weight range is between {min_weight:.1f} kg and {max_weight:.1f} kg."
                    )
                else:
                    user_inputs["target_weight"] = target_weight.value
                    bmi_warning.value = ""
                    next_step()
            except:
                bmi_warning.value = "Please enter a valid target weight."
            page.update()

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
            content=ft.Column(
                controls=[
                    # Header row
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                            ft.Text("Goal Setting", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                            ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    # Content center-aligned
                    ft.Container(
                        padding=ft.padding.only(top=150),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Text("Set your target weight", size=18, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK),
                                ft.Container(content=target_weight, alignment=ft.alignment.center),
                                bmi_warning
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),

                    # Bottom button
                    ft.Container(
                        padding=ft.padding.only(top=150),
                        content=ft.ElevatedButton(
                            text="Next",
                            on_click=check_target_bmi,
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

    def month_step():
        month_dropdown = ft.Dropdown(
            label="Select Duration (in months)",
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            width=300,
            color=ft.colors.BLACK,
            options=[ft.dropdown.Option(str(m)) for m in range(1, 13)],
            on_change=lambda e: selected_month_value.update({"value": e.control.value})
        )

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
            content=ft.Column(
                controls=[
                    # Header row
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_step, icon_color=ft.colors.BLACK),
                            ft.Text("Goal Setting", size=20, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                            ft.TextButton("Skip", on_click=next_step, style=ft.ButtonStyle(color=ft.colors.BLACK))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    # Main content
                    ft.Container(
                        padding=ft.padding.only(top=150),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "In how many months would you like to achieve your goal?",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    text_align="center",
                                    color=ft.colors.BLACK
                                ),
                                month_dropdown
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),

                    # Button near the bottom
                    ft.Container(
                        padding=ft.padding.only(top=180),
                        content=ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Next",
                                    on_click=lambda e: (
                                        user_inputs.update({"goal_duration": selected_month_value["value"]}),
                                        next_step(e)
                                    ),
                                    width=250,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.ORANGE,
                                        color=ft.colors.WHITE,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=15),
                                        shape=ft.RoundedRectangleBorder(radius=12)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    )
                ],
                spacing=25,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def complete_step():
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
            content=ft.Column(
                controls=[
                    # Header
                    ft.Stack(
                        controls=[
                            ft.Row(
                                [ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    on_click=back_step,
                                    icon_color=ft.colors.BLACK
                                )],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Row(
                                [ft.Text(
                                    "Goal Setting",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK,
                                    text_align="center"
                                )],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ]
                    ),

                    # Centered message and button
                    ft.Container(
                        padding=ft.padding.only(top=250),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Text("All set!", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                ft.Text("Your goals have been broken down into daily goals", size=14, color=ft.colors.BLACK)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        )
                    ),

                    # Continue button
                    ft.Container(
                        padding=ft.padding.only(top=20),
                        content=ft.ElevatedButton(
                            text="Continue",
                            on_click=lambda e: (save_to_csv(), page.go("/")),
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

    # Launch app at step 1
    go_to_step()

