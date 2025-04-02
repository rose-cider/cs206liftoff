import flet as ft
from login import render_login
from personality_quiz import render_quiz

def main(page: ft.Page):
    # Page configuration (matches both login and quiz styling)
    page.title = "LiftOff"
    page.window_width = 390
    page.window_height = 844
    page.window_frameless = True
    page.padding = 0
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Poppins")

    # Quiz completion handler
    def quiz_done_callback(personality):
        print(f"Quiz completed! Personality: {personality}")
        page.go("/home")  # Or wherever you want to go after quiz

    # Route handling
    def route_change(e):
        page.views.clear()
        
        if page.route == "/login":
            render_login(page)
        elif page.route == "/quiz":
            render_quiz(page, quiz_done_callback)
        elif page.route == "/home":
            show_home_page()
        else:
            page.go("/login")  # Default to login page

    def show_home_page():
        """Example home page navigation"""
        home_content = ft.Column([
            ft.Text("Welcome Home!", size=24),
            ft.ElevatedButton(
                "Take Quiz Again",
                on_click=lambda _: page.go("/quiz")
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        phone_frame = ft.Container(
            content=home_content,
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            padding=20,
            alignment=ft.alignment.center
        )
        
        page.views.append(ft.View("/home", [phone_frame]))
        page.update()

    # Setup routing
    page.on_route_change = route_change
    page.go("/login")  # Start with login page

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")