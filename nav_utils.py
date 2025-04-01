# nav_utils.py
import flet as ft

def create_navbar(active: str, on_nav: callable):
    def nav_icon(icon, label, target):
        is_active = active == target
        return ft.IconButton(
            icon=icon,
            icon_color="#FFFFFF" if is_active else "#FFE0B2",
            icon_size=24,
            on_click=lambda e: on_nav(target)
        )

    return ft.Container(
        content=ft.Row([
            nav_icon(ft.Icons.FITNESS_CENTER, "Workout", "workout"),
            nav_icon(ft.Icons.PERSON, "Profile", "profile"),
            nav_icon(ft.Icons.HOME, "Home", "home"),
            nav_icon(ft.Icons.TRACK_CHANGES, "Goals", "goals"),
            nav_icon(ft.Icons.SETTINGS, "Settings", "settings"),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        bgcolor="#FFA726",
        height=56,
        # padding=ft.padding.symmetric(vertical=4),
    )
