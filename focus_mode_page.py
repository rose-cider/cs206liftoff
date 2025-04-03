import flet as ft
import math
import asyncio
from header_utils import create_header
from nav_utils import create_navbar

def render_focus_mode(page: ft.Page):
    page.title = "Focus Mode"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    # Pull preview data from client_storage
    data = page.client_storage.get("workout_detail")
    if not data:
        page.go("/workout")
        return

    # Get character icon
    character_icons = {"Felix": "felix_icon.png", "Hammer": "hammer_icon.png", "Athena": "athena_icon.png"}
    user_personality = page.client_storage.get("user_personality") or "Felix"
    chosen_character = character_icons[user_personality]

    # Floating character
    character = ft.Image(src=chosen_character, width=80, height=80)
    character_container = ft.Container(content=character, alignment=ft.alignment.center, on_click=lambda e: page.go("/chat"))

    # Header
    header = create_header(
        "Focus Mode",
        on_back_click=lambda e: page.go("/workout"),
        show_felix=True,
        on_felix_click=lambda e: page.go("/chat"),
        icon=chosen_character
    )

    # Timer section with background image
    timer_section = ft.Stack([
        ft.Image(
            src=data["img_url"],
            width=390,
            height=260,
            fit=ft.ImageFit.COVER
        ),
        ft.Container(
            alignment=ft.alignment.center,
            content=ft.Container(
                width=200,
                height=200,
                border_radius=100,
                bgcolor=ft.colors.BLACK,
                border=ft.border.all(10, ft.colors.GREEN_400),
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(name=ft.icons.PAUSE, size=40, color=ft.colors.WHITE),
                    ft.Text("00:16:37", size=24, color=ft.colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
    ])

    # Goal summary
    goal_summary = ft.Container(
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.GREY_900),
        padding=15,
        border_radius=10,
        content=ft.Row([
            ft.Text("Goal:", size=16, color=ft.colors.GREY_700),
            ft.Text(f"{data['time']} min", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_700),
            ft.Text("•", size=16, color=ft.colors.GREY_600),
            ft.Text(f"{data['kcal']} cal", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_700),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    )

    # Encouragement message
    encouragement = ft.Container(
        padding=10,
        content=ft.Row([
            ft.Container(
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=10,
                on_click=lambda e: page.go("/buddy"),  # ✅ Go to buddy mode
                content=ft.Text("Wanna exercise together~", size=14)
            ),
            character_container
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # Main body
    focus_body = ft.Column([
        ft.Container(
            margin=0,
            alignment=ft.alignment.center,
            content=timer_section
        ),
        ft.Text(data["title"], size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(padding=ft.padding.symmetric(horizontal=20), content=goal_summary),
        ft.Container(padding=ft.padding.symmetric(horizontal=20), content=encouragement)
    ],
    spacing=20,
    alignment=ft.MainAxisAlignment.START,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    expand=True
    )

    nav_bar = create_navbar(
        active="workout",
        on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
    )

    # Page layout
    phone_layout = ft.Column([
        ft.Container(
            content=header,
            height=80,
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE
        ),
        ft.Container(
            expand=True,
            content=focus_body
        ),
        nav_bar
    ], spacing=0, tight=True)

    phone_frame = ft.Container(
        content=phone_layout,
        width=390,
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
        alignment=ft.alignment.center
    )

    centered_container = ft.Container(
        content=phone_frame,
        alignment=ft.alignment.center,
        expand=True
    )

    page.views.append(
        ft.View(
            "/focus",
            controls=[centered_container]
        )
    )
    page.update()

    # Floating animation
    async def float_character():
        t = 0
        while page.route == "/focus":
            character_container.offset = ft.Offset(0, 0.03 * math.sin(t))
            character_container.update()
            t += 0.2
            await asyncio.sleep(0.05)

    page.run_task(float_character)
