import flet as ft

def render_login(page: ft.Page, is_signup=False):
    page.views.clear()
    page.title = "LiftOff"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    # App Title (Orange)
    title = ft.Container(
        content=ft.Text("LiftOff", size=28, weight=ft.FontWeight.BOLD, color="#FFA726"),
        alignment=ft.alignment.center,
        padding=15,
    )

    # Dynamic header (Login / Sign Up), left-aligned
    header_text = "Sign Up" if is_signup else "Login"
    header = ft.Container(
        content=ft.Text(header_text, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(left=10, bottom=5),
    )

    # Input fields
    email_input = ft.TextField(label="Email", bgcolor=ft.Colors.WHITE)
    password_input = ft.TextField(label="Password", password=True, bgcolor=ft.Colors.WHITE)

    # Extra field for signup
    name_input = ft.TextField(label="Full Name", bgcolor=ft.Colors.WHITE) if is_signup else None

    # Submit button (Login → Home | Sign Up → Quiz)
    action_text = "Sign Up" if is_signup else "Login"
    action_route = "/quiz" if is_signup else "/"

    action_button = ft.Container(
        content=ft.Row([
            ft.Text(action_text, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="#FFA726",
        border_radius=10,
        padding=12,
        expand=True,
        margin=6,
        on_click=lambda e: page.go(action_route),  # Redirects based on login or signup
    )

    # Toggle between login and signup
    switch_text = "Already have an account? Login" if is_signup else "Don't have an account? Sign up"
    switch_button = ft.TextButton(switch_text, on_click=lambda e: render_login(page, not is_signup))

    # Form content centered inside the phone
    form_items = [email_input, password_input, action_button, switch_button]
    if is_signup:
        form_items.insert(0, name_input)  # Add name field for signup

    form_section = ft.Container(
        content=ft.Column(form_items, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center,
    )

    # Phone frame
    phone_content = ft.Column([
        title,
        header,
        ft.Container(content=form_section, alignment=ft.alignment.center),  # Center form in phone
    ], spacing=0, tight=True)

    # Updated phone frame (matches render_goals)
    phone_frame = ft.Container(
        content=phone_content,
        width=390,
        height=844,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
    )

    centered_container = ft.Container(
        content=phone_frame,
        alignment=ft.alignment.center,
        expand=True,
    )

    page.views.append(ft.View("/login", [centered_container]))
    page.update()
