import flet as ft
from header_utils import create_header
from nav_utils import create_navbar

def render_workout_detail(page: ft.Page, chosen_character=None):
    data = page.client_storage.get("workout_detail")
    page.title = "Workout Detail"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    character_icons = {
        "Felix": "felix_icon.png",
        "Hammer": "hammer_icon.png",
        "Athena": "athena_icon.png"
    }
    chosen_character = character_icons.get(chosen_character, "felix_icon.png")

    if not data:
        page.go("/workout")
        return

    workout_header = create_header(
        "Workout Detail",
        on_back_click=lambda e: page.go("/"),
        show_felix=True,
        on_felix_click=lambda e: page.go("/chat"),
        icon=chosen_character
    )

    workout_image = ft.Image(
        src=data["img_url"],
        width=390,
        height=180,
        fit=ft.ImageFit.COVER
    )

    workout_info = ft.Column([
        ft.Text(data["title"], size=24, weight=ft.FontWeight.BOLD),
        ft.Text(f'{data["kcal"]} kcal • {data["time"]} min', size=14, italic=True, color=ft.colors.GREY),
        ft.Divider(),
        ft.Text(data["description"], size=16),
        ft.Container(
            margin=10,
            padding=10,
            bgcolor=ft.colors.GREY_100,
            border_radius=10,
            content=ft.Column([
                ft.Text("Session Timeline", weight=ft.FontWeight.BOLD, size=18),
                ft.Divider(),
                ft.ListTile(title=ft.Text("Warm-up"), subtitle=ft.Text("5 minutes")),
                ft.ListTile(title=ft.Text("Basic jabs"), subtitle=ft.Text("10 minutes")),
                ft.ListTile(title=ft.Text("Combos practice"), subtitle=ft.Text("10 minutes")),
                ft.ListTile(title=ft.Text("Footwork drills"), subtitle=ft.Text("10 minutes")),
                ft.ListTile(title=ft.Text("Cool down"), subtitle=ft.Text("5 minutes")),
            ])
        ),
        ft.Container(
            alignment=ft.alignment.center,
            margin=20,
            content=ft.ElevatedButton(
                "Start Workout",
                icon=ft.icons.FITNESS_CENTER,
                on_click=lambda e: page.go("/focus")
            )
        )
    ])

    scrollable_body = ft.Column(
        controls=[
            workout_image,
            ft.Container(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                content=workout_info
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    bottom_nav = create_navbar(
        active="workout",
        on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
    )

    phone_layout = ft.Column([
        ft.Container(
            content=workout_header,
            height=80,
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE
        ),
        scrollable_body,
        bottom_nav
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
            "/workout-detail",
            controls=[centered_container]
        )
    )
    page.update()






