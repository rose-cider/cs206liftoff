import flet as ft
from header_utils import create_header
from nav_utils import create_navbar

def render_workout(page: ft.Page):
    page.title = "Today's Workout"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    # Header styled like home
    workout_header = create_header("Workout", on_back_click=lambda e: page.go("/"),
    show_felix=True,
    on_felix_click=lambda e: page.go("/felix"))

    # Reusable goal widget
    def goal_circle(label: str, value: str):
        return ft.Column([
            ft.Container(
                width=60,
                height=60,
                border_radius=30,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(4, ft.Colors.GREEN),
                alignment=ft.alignment.center,
                content=ft.Text(value, weight=ft.FontWeight.BOLD, size=10, text_align=ft.TextAlign.CENTER),
                margin=ft.margin.only(bottom=4),
            ),
            ft.Text(label, size=11, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Goal section
    goal_section = ft.Container(
        bgcolor="#FFA726",
        padding=20,
        content=ft.Column([
            ft.Text("Goal of the day", weight=ft.FontWeight.BOLD, size=16, text_align=ft.TextAlign.CENTER),
            ft.Row([
                goal_circle("Steps", "1,5000\nstep"),
                goal_circle("Calories", "3000\ncal"),
                goal_circle("Time", "2 hours"),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ])
    )

    # Workout card
    def session_card(title, kcal, time, img_url):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=10,
            content=ft.Column([
                ft.Image(src=img_url, width=300, height=100, border_radius=10, fit=ft.ImageFit.COVER),
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, size=16, color="#FFA726"),
                        ft.Text(f"{kcal} kcal", size=12),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, size=16, color="#FFA726"),
                        ft.Text(f"{time} min", size=12),
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )

    # Workout session list
    session_section = ft.Column([
        ft.Row([
            ft.Text("Session of the day", weight=ft.FontWeight.BOLD, size=14),
            ft.Text("View All", color=ft.Colors.BLUE, size=12),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        session_card("Quick Warm Up", 125, 20, "https://picsum.photos/300/100?1"),
        session_card("Arm Strengthening", 125, 50, "https://picsum.photos/300/100?2"),
        session_card("Shadow Boxing", 125, 40, "https://picsum.photos/300/100?3"),
        ft.Container(
            bgcolor=ft.Colors.BLUE_50,
            padding=10,
            border_radius=5,
            content=ft.Text("📝 Notes: You have not yet completed your session of the day.")
        )
    ], spacing=10)

    # Bottom nav
    bottom_nav = create_navbar(
        active="workout",
        on_nav=lambda target: page.go("/" if target == "home" else f"/{target}")
    )

    # ✅ Scrollable center section
    scrollable_body = ft.Column(
        controls=[
            goal_section,
            ft.Container(content=session_section, padding=15, bgcolor=ft.Colors.WHITE),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # Phone layout
    phone_content = ft.Column([
        # Top notch
        ft.Container(
            content=ft.Row([
                ft.Container(
                    width=100,
                    height=20,
                    border_radius=ft.border_radius.only(bottom_right=12, bottom_left=12),
                    bgcolor="#000000",
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#000000",
            height=28,
        ),
        workout_header,       # fixed
        scrollable_body,      # scrolls
        bottom_nav            # fixed
    ], spacing=0, tight=True)

    phone_frame = ft.Container(
        content=phone_content,
        width=390,
        height=844,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(12, "#000000"),
        border_radius=40,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.5, "#000000"),
            offset=ft.Offset(0, 5),
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    phone_with_buttons = ft.Stack([
        ft.Container(content=phone_frame, alignment=ft.alignment.center),
        ft.Container(width=3, height=30, bgcolor="#000000", border_radius=5, left=0, top=150),
        ft.Container(width=3, height=30, bgcolor="#000000", border_radius=5, left=0, top=190),
        ft.Container(width=3, height=40, bgcolor="#000000", border_radius=5, right=0, top=170),
    ])

    centered_container = ft.Container(
        content=phone_with_buttons,
        alignment=ft.alignment.center,
        expand=True,
    )

    page.views.append(ft.View("/workout", [centered_container]))
    page.update()



