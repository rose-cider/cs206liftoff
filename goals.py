import flet as ft

from nav_utils import create_navbar
from header_utils import create_header

def render_goals(page: ft.Page, selected_tab_index=0):
    page.title = "Goals"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = color.WHITE

    # Header styled like home
    goals_header = create_header("Goals", on_back_click=lambda e: page.go("/"),
    show_felix=True,
    on_felix_click=lambda e: page.go("/felix"))

    def update_tab(index):
        page.clean()
        render_goals(page, selected_tab_index=index)

    def tab_selector():
        return Container(
            margin=margin.only(top=10),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Tabs(
                        selected_index=selected_tab_index,
                        animation_duration=300,
                        on_change=lambda e: update_tab(e.control.selected_index),
                        tabs=[
                            Tab(text="Weekly"),
                            Tab(text="End goal"),
                        ],
                        expand=False,
                        indicator_color="#FFA726",
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
            border=border.all(1, color=colors.BLACK12),
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
                                    color="#FFA726",
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
                                            Text("600 kcal", size=24, weight="bold"),
                                            Text("/1400 kcal", size=18, color=colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    Container(
                        bgcolor="#FFA726",
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
                                    src="felix_icon.png",
                                    width=60,
                                    height=60,
                                    fit=ImageFit.CONTAIN,
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
            border=border.all(1, color=colors.BLACK12),
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
                                    value=0.75,
                                    stroke_width=15,
                                    color="#FFA726",
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
                                            Text("11250 kcal", size=24, weight="bold"),
                                            Text("/15000 kcal", size=18, color=colors.BLACK54),
                                        ]
                                    ),
                                ),
                            ],
                        )
                    ),
                    Container(
                        bgcolor="#FFA726",
                        border_radius=10,
                        padding=padding.all(15),
                        content=Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(
                                    "You're 75% there!\nKeep up the momentum!",
                                    color=colors.WHITE,
                                    size=16,
                                    weight="w500",
                                ),
                                Image(
                                    src="felix_icon.png",
                                    width=60,
                                    height=60,
                                    fit=ImageFit.CONTAIN,
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
                style=ButtonStyle(
                    bgcolor={"": "#FFA726"},
                    shape=RoundedRectangleBorder(radius=10),
                    padding=padding.all(20),
                ),
                width=350
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
                style=ButtonStyle(
                    bgcolor={"": "#FFA726"},
                    shape=RoundedRectangleBorder(radius=10),
                    padding=padding.all(20),
                ),
                width=350,
            )
        )

    # Scrollable content area
    scrollable_body = Column(
        controls=[
            tab_selector(),
            goal_progress() if selected_tab_index == 0 else end_goal_progress(),
            view_progress_button(),
            edit_goal_button(),
            #Container(height=20),
        ],
        scroll=ScrollMode.AUTO,
        expand=True,
    )

    phone_content = Column([
        # Container(
        #     content=Row([
        #         Container(
        #             width=100,
        #             height=20,
        #             border_radius=ft.border_radius.only(bottom_right=12, bottom_left=12),
        #             bgcolor="#000000",
        #         )
        #     ], alignment=MainAxisAlignment.CENTER),
        #     bgcolor="#000000",
        #     height=28,
        # ),
        Container(
            content = goals_header,
            height = 80,
            padding = padding.all(10),
            bgcolor = ft.colors.WHITE,
        ),
        scrollable_body,
        create_navbar(
            active="goals",
            on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
        )
    ], spacing=0, tight=True)

    phone_frame = Container(
        content=phone_content,
        width=390,
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
        alignment=ft.alignment.center,
    )

    page.add(phone_frame)