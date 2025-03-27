import flet as ft
from flet import (
    Page, Container, Column, Row, Text, Icon, IconButton,
    ElevatedButton, Image, ProgressRing, Tabs, Tab,
    MainAxisAlignment, CrossAxisAlignment, BorderRadius,
    Alignment, padding, margin, colors, Stack, Ref
)

def main(page: Page):
    page.title = "Fitness App"
    page.padding = 0
    page.window_width = 430
    page.window_height = 930
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = colors.WHITE

    selected_tab = Ref[int]()
    selected_tab.value = 0

    def status_bar():
        return Container(
            padding=padding.only(left=20, right=20, top=10, bottom=10),
            bgcolor=colors.WHITE,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("9:41", size=16, weight="bold"),
                    Row(
                        spacing=8,
                        controls=[
                            Icon(ft.icons.SIGNAL_CELLULAR_ALT, size=16),
                            Icon(ft.icons.WIFI, size=16),
                            Icon(ft.icons.BATTERY_FULL, size=16),
                        ]
                    )
                ]
            )
        )

    def header():
        return Container(
            padding=padding.only(left=20, right=20, top=15, bottom=15),
            bgcolor=colors.WHITE,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color=colors.BLACK,
                        icon_size=24,
                    ),
                    Text("Goals", size=20, weight="bold"),
                    Container(
                        width=40,
                        height=40,
                        border_radius=20,
                        bgcolor="#F2C05B",
                        content=Image(
                            src="hammer_icon.png",
                            width=30,
                            height=30,
                            fit=ft.ImageFit.CONTAIN,
                        )
                    )
                ]
            )
        )

    def tab_selector():
        return Container(
            margin=margin.only(top=10),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Tabs(
                        selected_index=selected_tab.value,
                        animation_duration=300,
                        on_change=lambda e: update_tab(e.control.selected_index),
                        tabs=[
                            Tab(text="Weekly"),
                            Tab(text="End goal"),
                        ],
                        expand=False,
                        indicator_color="#E2A845",  # 🔸 ORANGE indicator
                        indicator_thickness=3,
                        label_color=colors.BLACK,
                        unselected_label_color=colors.BLACK54
                    )
                ]
            )
        )

    def goal_progress():
        return Container(
            margin=margin.only(left=20, right=20, top=20),
            padding=padding.all(20),
            border=ft.border.all(1, color=colors.BLACK12),
            border_radius=20,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("Burn 1400 kcal per week", size=22, weight="bold"),
                    Container(
                        margin=margin.only(top=20, bottom=20),
                        content=Stack(
                            controls=[
                                ProgressRing(
                                    width=200,
                                    height=200,
                                    value=0.43,
                                    stroke_width=15,
                                    color="#E2A845",
                                    bgcolor=colors.BLACK12,
                                ),
                                Container(
                                    width=200,
                                    height=200,
                                    alignment=Alignment(0, 0),
                                    content=Column(
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Text("600 cal", size=24, weight="bold"),
                                            Text("/1400 cal", size=18, color=colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    Container(
                        bgcolor="#E2A845",
                        border_radius=10,
                        padding=padding.all(15),
                        content=Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(
                                    "You have burnt 600 kcal\nin 3 days! Keep it up!",
                                    color=colors.WHITE,
                                    size=16,
                                    weight="w500",
                                ),
                                Image(
                                    src="hammer_icon.png",
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
        return Container(
            margin=margin.only(left=20, right=20, top=20),
            padding=padding.all(20),
            border=ft.border.all(1, color=colors.BLACK12),
            border_radius=20,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("Burn 8000 kcal total", size=22, weight="bold"),
                    Container(
                        margin=margin.only(top=20, bottom=20),
                        content=Stack(
                            controls=[
                                ProgressRing(
                                    width=200,
                                    height=200,
                                    value=0.75,  # example: 6000/8000
                                    stroke_width=15,
                                    color="#E2A845",
                                    bgcolor=colors.BLACK12,
                                ),
                                Container(
                                    width=200,
                                    height=200,
                                    alignment=Alignment(0, 0),
                                    content=Column(
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Text("6000 cal", size=24, weight="bold"),
                                            Text("/8000 cal", size=18, color=colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    Container(
                        bgcolor="#E2A845",
                        border_radius=10,
                        padding=padding.all(15),
                        content=Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(
                                    "You're 75% there!\nKeep up the momentum 💪",
                                    color=colors.WHITE,
                                    size=16,
                                    weight="w500",
                                ),
                                Image(
                                    src="hammer_icon.png",
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

    def view_progress_button():
        return Container(
            margin=margin.only(left=20, right=20, top=20),
            content=ElevatedButton(
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text("View Progress", color=colors.WHITE, size=18, weight="w500"),
                        Icon(ft.icons.CHEVRON_RIGHT, color=colors.WHITE),
                    ]
                ),
                style=ft.ButtonStyle(
                    bgcolor={"": "#E2A845"},
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=padding.all(20),
                ),
                width=page.window_width - 40,
            )
        )

    def edit_goal_button():
        return Container(
            margin=margin.only(left=20, right=20, top=10),
            content=ElevatedButton(
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text("Edit Goal", color=colors.WHITE, size=18, weight="w500"),
                        Icon(ft.icons.EDIT, color=colors.WHITE),
                    ]
                ),
                style=ft.ButtonStyle(
                    bgcolor={"": "#E2A845"},
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=padding.all(20),
                ),
                width=page.window_width - 40,
            )
        )

    def update_tab(index):
        selected_tab.value = index
        page.controls.clear()
        build_page()
        page.update()

    def build_page():
        content_column = Column(
            spacing=0,
            controls=[
                status_bar(),
                header(),
                tab_selector(),
                goal_progress() if selected_tab.value == 0 else end_goal_progress(),
                view_progress_button(),
                edit_goal_button(),
                Container(height=20),
            ]
        )

        # Create a phone-size frame for consistent layout
        phone_frame = Container(
            content=content_column,
            width=390,
            height=844,
            bgcolor=colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, colors.GREY_300),
            alignment=ft.alignment.top_center
        )

        # Center the phone frame on the page
        page.add(
            Container(
                content=phone_frame,
                alignment=ft.alignment.center,
                expand=True
            )
        )

    build_page()

ft.app(target=main)
