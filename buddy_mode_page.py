import flet as ft
import math
import asyncio
from header_utils import create_header
from nav_utils import create_navbar

def render_buddy_mode(page: ft.Page):
    page.title = "Buddy Mode"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFA726"

    data = page.client_storage.get("workout_detail")
    if not data:
        page.go("/workout")
        return

    character_icons = {
        "Felix": "felix_icon.png",
        "Hammer": "hammer_icon.png",
        "Athena": "athena_icon.png"
    }
    user_personality = page.client_storage.get("user_personality") or "Felix"
    chosen_character = character_icons[user_personality]

    character = ft.Image(src=chosen_character, width=140, height=140)
    character_container = ft.Container(content=character, alignment=ft.alignment.center)

    header = create_header(
        "Buddy Mode",
        on_back_click=lambda e: page.go("/focus"),
        show_felix=True,
        on_felix_click=lambda e: page.go("/chat"),
        icon=chosen_character
    )

    motivational_bubble = ft.Container(
        padding=15,
        border_radius=15,
        margin=ft.margin.only(bottom=10),
        bgcolor=ft.colors.with_opacity(0.3, ft.colors.BROWN),
        content=ft.Text(
            "You've got this!\nJust one more set to go!",
            size=16,
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.WHITE
        )
    )

    timer_display = ft.Text("00:16:37", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    session_text = ft.Text(f"Session 3 - {data['title']}", size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)

    goal_display = ft.Container(
        bgcolor=ft.colors.GREY_200,
        padding=15,
        border_radius=10,
        content=ft.Row([
            ft.Text("Goal:", color=ft.colors.GREY_700),
            ft.Text(f"{data['time']} min", weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_700, size=14),
            ft.Text(" • ", color=ft.colors.GREY_400),
            ft.Text(f"{data['kcal']} cal", weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_700, size=14),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        width=300
    )

    nav_bar = ft.Container(
        content=create_navbar(
            active="workout",
            on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
        ),
        bgcolor="#FFA726"
    )

    phone_content = ft.Column([
        ft.Container(content=header, height=80, padding=ft.padding.all(10), bgcolor=ft.colors.WHITE),
        ft.Container(
            expand=True,
            padding=20,
            bgcolor="#FFA726",
            content=ft.Column([
                motivational_bubble,
                character_container,
                timer_display,
                session_text,
                goal_display
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ),
        nav_bar
    ], spacing=0, tight=True)

    page.views.append(
        ft.View(
            "/buddy",
            controls=[
                ft.Container(
                    content=ft.Container(
                        content=phone_content,
                        width=390,
                        height=844,
                        bgcolor=ft.colors.WHITE,
                        border_radius=20,
                        border=ft.border.all(2, ft.colors.GREY_300),
                        alignment=ft.alignment.center
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )
    )
    page.update()

    async def float_character():
        t = 0
        while page.route == "/buddy":
            character_container.offset = ft.Offset(0, 0.03 * math.sin(t))
            character_container.update()
            t += 0.2
            await asyncio.sleep(0.05)

    page.run_task(float_character)

