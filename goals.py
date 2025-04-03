import flet as ft

from nav_utils import create_navbar
from header_utils import create_header

def render_goals(page: ft.Page, selected_tab_index=0, chosen_character=None):
    page.title = "Goals"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE

    character_icons = {
        "Felix": "felix_icon.png",
        "Hammer": "hammer_icon.png",
        "Athena": "athena_icon.png"
    }
    chosen_icon = character_icons[chosen_character]

    # Header styled like home
    goals_header = create_header(
        "Goals",
        on_back_click=lambda e: page.go("/"),
        show_felix=True,
        on_felix_click=lambda e: page.go("/chat"),
        icon=chosen_icon
    )

    def update_tab(index):
        page.clean()
        render_goals(page, selected_tab_index=index, chosen_character=chosen_character)

    def tab_selector():
        return ft.Container(
            margin=ft.margin.only(top=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Tabs(
                        selected_index=selected_tab_index,
                        animation_duration=300,
                        on_change=lambda e: update_tab(e.control.selected_index),
                        tabs=[
                            ft.Tab(text="Weekly"),
                            ft.Tab(text="End goal"),
                        ],
                        expand=False,
                        indicator_color="#FFA726",
                        indicator_thickness=3,
                        label_color=ft.colors.BLACK,
                        unselected_label_color=ft.colors.BLACK54
                    )
                ]
            )
        )

    def goal_progress():
        return ft.Container(
            margin=ft.margin.only(left=20, right=20, top=20),
            padding=ft.padding.all(20),
            border=ft.border.all(1, color=ft.colors.BLACK12),
            border_radius=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Burn 1400 kcal per week", size=22, weight="bold"),
                    ft.Container(
                        margin=ft.margin.only(top=20, bottom=20),
                        content=ft.Stack(
                            controls=[
                                ft.ProgressRing(
                                    width=200,
                                    height=200,
                                    value=0.43,
                                    stroke_width=15,
                                    color="#FFA726",
                                    bgcolor=ft.colors.BLACK12,
                                ),
                                ft.Container(
                                    width=200,
                                    height=200,
                                    alignment=ft.alignment.center,
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("600 kcal", size=24, weight="bold"),
                                            ft.Text("/1400 kcal", size=18, color=ft.colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    ft.Container(
                        bgcolor="#FFA726",
                        border_radius=10,
                        padding=ft.padding.all(15),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "You have burnt 600 kcal\nin 3 days! Keep it up!",
                                    color=ft.colors.WHITE,
                                    size=16,
                                    weight="w500",
                                ),
                                ft.Image(
                                    src="felix_icon.png",
                                    width=60,
                                    height=60,
                                    fit=ft.ImageFit.CONTAIN,
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def end_goal_progress():
        return ft.Container(
            margin=ft.margin.only(left=20, right=20, top=20),
            padding=ft.padding.all(20),
            border=ft.border.all(1, color=ft.colors.BLACK12),
            border_radius=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Complete 10,000 steps daily", size=22, weight="bold"),
                    ft.Container(
                        margin=ft.margin.only(top=20, bottom=20),
                        content=ft.Stack(
                            controls=[
                                ft.ProgressRing(
                                    width=200,
                                    height=200,
                                    value=0.0,  # Placeholder progress value
                                    stroke_width=15,
                                    color="#4CAF50",
                                    bgcolor=ft.colors.BLACK12,
                                ),
                                ft.Container(
                                    width=200,
                                    height=200,
                                    alignment=ft.alignment.center,
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("0 steps", size=24, weight="bold"),
                                            ft.Text("/10,000 steps", size=18, color=ft.colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    ft.Container(
                        bgcolor="#4CAF50",
                        border_radius=10,
                        padding=ft.padding.all(15),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Track your daily steps\nto reach your end goal!",
                                    color=ft.colors.WHITE,
                                    size=16,
                                    weight="w500",
                                ),
                                ft.Image(
                                    src="steps_icon.png",
                                    width=60,
                                    height=60,
                                    fit=ft.ImageFit.CONTAIN
                                )
                            ]
                        )
                    )
                ]
            )
        )

    scrollable_body = ft.Column(
        controls=[
            tab_selector(),
            goal_progress() if selected_tab_index == 0 else end_goal_progress(),
        ],
        scroll = ft.ScrollMode.AUTO,
        expand=True
    )

    phone_content = ft.Column([
        ft.Container(
            content=goals_header,
            height=80,
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE,
        ),
        scrollable_body,
        create_navbar(
            active="goals",
            on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
        )
    ], spacing=0, tight=True)

    phone_frame = ft.Container(
        content=phone_content,
        width=390,
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
        alignment=ft.alignment.center,
    )

    page.views.append(ft.View("/goals", [phone_frame]))
    page.update()