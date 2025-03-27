# header_utils.py
import flet as ft

def create_header(title: str, show_back: bool = True, on_back_click=None, show_felix: bool = True, on_felix_click=None):
    return ft.Container(
        content=ft.Row([
            # Back button or empty space
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ft.Colors.BLACK,
                visible=show_back,
                on_click=on_back_click
            ) if show_back else ft.Container(width=40),

            # Center title
            ft.Text(
                title,
                weight=ft.FontWeight.BOLD,
                size=18,
                expand=True,
                text_align=ft.TextAlign.CENTER
            ),

            # Felix icon or empty container to preserve layout
            ft.Container(
                content=(
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Image(src="felix_icon.png", width=30, height=30),
                            bgcolor="#FFA726",
                            padding=6,
                            border_radius=30,
                        ),
                        on_tap=on_felix_click
                    )
                ) if show_felix else ft.Container(width=42)  # preserve layout spacing
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.BLACK12)),
    )

