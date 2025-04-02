import flet as ft
from flet import *
import math
import asyncio
from header_utils import create_header
from nav_utils import create_navbar

def render_home(page: ft.Page, chosen_character="Felix"):
    page.views.clear()
    page.title = "Lift Off"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    character_icons = {"Felix": "felix_icon.png", "Hammer": "hammer_icon.png","Athena": "athena_icon.png"}
    chosen_character = character_icons[chosen_character]

    character = ft.Image(src=chosen_character, width=100, height=100)
    character_container = ft.Container(content=character, alignment=ft.alignment.center)

    header = create_header("Lift Off", show_back=False, show_felix=False)

    welcome_section = ft.Container(
        content=ft.Column([
            ft.Text("Welcome back, Joey!", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Row([
                ft.Column([
                    ft.Container(
                        content=ft.Text("Ready to crush today's workout?", color=ft.Colors.BLACK),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=8,
                        margin=ft.margin.only(bottom=6),
                    ),
                    ft.Container(
                        content=ft.Text("Just 5 more days to reach your goal!", color=ft.Colors.BLACK),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=8,
                        margin=ft.margin.only(bottom=6),
                    ),
                    ft.Container(
                        content=ft.Text("Keep going!", color=ft.Colors.BLACK),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        padding=8,
                    ),
                ], expand=True),
                character_container,
            ]),
        ], spacing=15),
        bgcolor="#FFA726",
        padding=15,
    )

    action_buttons = ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PLAY_CIRCLE, color=ft.Colors.WHITE, size=20),
                ft.Text("Start!", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#FFA726",
            border_radius=10,
            padding=12,
            expand=True,
            margin=6,
            on_click=lambda e: page.go("/workout")
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.REFRESH, color="#FFA726", size=20),
                ft.Text("Change of Plan", color="#FFA726", weight=ft.FontWeight.BOLD, size=14),
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, "#FFA726"),
            border_radius=10,
            padding=12,
            expand=True,
            margin=6,
        ),
    ])

    status_section = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color="#FFA726"),
                    margin=ft.margin.only(right=10),
                ),
                ft.Column([
                    ft.Text("My status", weight=ft.FontWeight.BOLD),
                    ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color="#FFA726", size=14)]),
                ], spacing=4),
                ft.Container(
                    content=ft.Column([
                        ft.Text("20", weight=ft.FontWeight.BOLD, size=20),
                        ft.Text("Day Streak", size=11),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    margin=ft.margin.only(left=80),
                ),
                ft.Icon(ft.Icons.STAR, color="#FFA726", size=20),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(height=16, color=ft.Colors.BLACK12),
            ft.Row([
                ft.Column([
                    ft.Icon(ft.Icons.DIRECTIONS_WALK, color=ft.Colors.BLACK54),
                    ft.Text("1,243", weight=ft.FontWeight.BOLD),
                    ft.Text("Steps", size=11),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.VerticalDivider(width=1, color=ft.Colors.BLACK12),
                ft.Column([
                    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED),
                    ft.Text("50", weight=ft.FontWeight.BOLD),
                    ft.Text("bpm", size=11),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.VerticalDivider(width=1, color=ft.Colors.BLACK12),
                ft.Column([
                    ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE),
                    ft.Text("283", weight=ft.FontWeight.BOLD),
                    ft.Text("cal", size=11),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        ]),
        padding=15,
    )

    bottom_nav = create_navbar(
        active="home",
        on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
    )

    scrollable_content = ft.Container(
        content=ft.Column([
            welcome_section,
            action_buttons,
            status_section,
        ], scroll=ft.ScrollMode.AUTO),
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
            content = header,
            height = 80,
            padding = padding.all(10),
            bgcolor = ft.colors.WHITE,
        ),
        scrollable_content,
        bottom_nav
    ], spacing=0, tight=True)

    phone_frame = ft.Container(
        content=phone_content,
        width=390,  # Match dimensions from render_goals
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,  # Match rounded corners from render_goals
        border=ft.border.all(2, ft.colors.GREY_300),  # Match border style
        alignment=ft.alignment.center,
    )

    centered_container = ft.Container(
        content=phone_frame,
        alignment=ft.alignment.center,
        expand=True,
    )

        # Add content to the page
    page.views.append(ft.View("/", [centered_container]))
    page.update()

    # Animate Charatcter AFTER adding to the page
    async def float_character():
        t = 0
        while True:
            if page.route != "/":
                break
            character_container.offset = ft.Offset(0, 0.03 * math.sin(t))
            character_container.update()
            t += 0.2
            await asyncio.sleep(0.05)

    async def delayed_character_animation():
        await asyncio.sleep(0.1)
        await float_character()

    page.run_task(delayed_character_animation)







