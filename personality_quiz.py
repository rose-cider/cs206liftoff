import flet as ft
import os
from header_utils import create_header  # You can remove this line
from nav_utils import create_navbar  # You can remove this line

global personality
personality = None

class PersonalityQuiz:
    def __init__(self):
        self.questions = [
            "How would you describe your work ethic?",
            "Would a strict teacher motivate you to achieve your goals?",
            "How do you react to missing a workout?",
            "What motivates you to push through tough exercises?",
            "What do you value most in a workout buddy?"
        ]

        self.options = [
            ["Methodical and steady.", "Decently productive but with the tendency to lose motivation...", "Unpredictable and spontaneous."],
            ["Yes! A little strictness is what I need to do my best.", "It makes me less motivated or maybe even annoyed...", "I need lots of firm guidance to get anything done."],
            ["I need a firm push to get back on track and not lose progress.", "I'd appreciate talking through what went wrong and adjusting the plan.", "I prefer reflecting on it myself and figuring out how to move forward."],
            ["A strict reminder of my goals and why I need to stick to the plan.", "A discussion on how the workout benefits me, so I stay engaged...", "The freedom to choose myself."],
            ["A tough, no-nonsense approach that reminds me to stay focussed.", "Positive reinforcement and a conversation about my progress.", "Gentle suggestions and leaving me to motivate myself."],
            ["Someone who is firm and keeps me disciplined.", "Someone who can explain why we're doing certain exercises and listens to my feedback.", "Someone who lets me figure things out!"]]

        self.current_question = 0
        self.answers = []
        self.quiz_done_callback = None  # Callback function
        self.page = None  # Store the page object

    def main(self, page: ft.Page, quiz_done_callback=None):
        self.page = page  # Store the page object
        self.quiz_done_callback = quiz_done_callback
        page.title = "Personality Quiz"
        page.window_width = 390
        page.window_height = 844
        page.window_frameless = True

        # Enable scrolling on the page
        page.scroll = ft.ScrollMode.ADAPTIVE  # Or .ALWAYS

        # Custom header row
        self.quiz_header_row = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.previous_question, icon_color=ft.colors.BLACK),  # Use self.previous_question
                ft.Text("Personality Quiz", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.TextButton("Skip", on_click=self.skip_quiz, style=ft.ButtonStyle(color=ft.colors.BLACK))  # Use self.skip_quiz
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Start Page Elements
        self.start_header = ft.Text(
            "We're exhilarated that you've joined us!",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        self.start_description = ft.Text(
            "But before we start, we need to understand you better. Let's do a short personality quiz that will determine the best LiftOff gym buddy for you. For each of these questions, pick the answer that most closely resembles you.",
            size=16,
            text_align=ft.TextAlign.CENTER
        )
        self.start_button = ft.ElevatedButton(
            text="OK!",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
            on_click=self.start_quiz
        )

        # Start Page Layout
        self.start_page_content = ft.Column(
            [
                ft.Container(expand=1),
                self.start_header,
                ft.Container(height=20),
                self.start_description,
                ft.Container(expand=True),
                self.start_button,
                ft.Container(expand=1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )

        # Question text container with padding for aesthetics
        self.question_text = ft.Text(
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        # Option buttons with padding inside buttons for spacing
        self.option_buttons = [
            ft.ElevatedButton(
                text=f"Option {i+1}",
                on_click=self.next_question,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.all(20),  # Add padding inside buttons
                ),
                bgcolor="#FFA726",
                color="white",
                width=350,
            ) for i in range(3)
        ]
        # Back button (hidden initially)
        self.back_button = ft.ElevatedButton(
            text="Back",
            on_click=self.previous_question,
            visible=False,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
        )

        # Quiz view layout (Include the custom header)
        self.quiz_view = ft.Column(
            [
                self.quiz_header_row,  # Add the custom header row
                ft.Container(content=self.question_text, padding=ft.padding.only(top=50)),  # Padding for question text
                ft.Column(self.option_buttons, spacing=10),
                ft.Container(height=20),  # Spacer
                self.back_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )

        # Result view layout (hidden initially)
        self.result_header = ft.Text()
        self.result_image = ft.Image()
        self.result_description = ft.Text()
        self.next_button = ft.ElevatedButton(
            text="Next",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
                padding=20  # Padding for internal spacing inside button
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
            on_click=self.go_to_chat  # Show the Info Steps
        )

        self.result_view = ft.Column(
            [
                ft.Container(expand=1),
                self.result_header,
                self.result_image,
                self.result_description,
                ft.Container(expand=True),  # Pushes next button to bottom
                self.next_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )

        # Wrap each step in a phone frame container
        self.phone_frame_start_page = ft.Container(
            content=self.start_page_content,
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            alignment=ft.alignment.center,
            visible=True,  # Make sure the initial one is visible
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
        )

        self.phone_frame_quiz_view = ft.Container(
            content=self.quiz_view,
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            alignment=ft.alignment.center,
            visible=False,
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
        )

        self.phone_frame_result_view = ft.Container(
            content=self.result_view,
            width=390,
            height=844,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(2, ft.colors.GREY_300),
            alignment=ft.alignment.center,
            visible=False,
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
        )

        # Make main_column a Stack and control visibility of frames
        self.main_column = ft.Stack(
            [self.phone_frame_start_page, self.phone_frame_quiz_view, self.phone_frame_result_view],
            expand=True
        )

        page.add(self.main_column)

        # This function moves the visibility of each component, depending on the button pressed

    def start_quiz(self, e):
        """Handle starting the quiz."""
        self.phone_frame_start_page.visible = False
        self.phone_frame_quiz_view.visible = True
        self.update_question()
        if self.page:
            self.page.update()

    def update_question(self):
        """Update the current question and options."""
        self.question_text.value = self.questions[self.current_question]
        # Update option buttons' text
        for i, button in enumerate(self.option_buttons):
            button.text = self.options[self.current_question][i]
        # Show/hide back button based on question index
        self.back_button.visible = self.current_question > 0
        # Update quiz view UI
        self.quiz_view.update()
        if self.page:
            self.page.update()

    def next_question(self, e):
        """Handle moving to the next question or showing results."""
        selected_option_index = next(i for i, btn in enumerate(self.option_buttons) if btn == e.control)
        # Save user's answer
        self.answers.append(selected_option_index)
        if self.current_question < len(self.questions) - 1:
            # Move to next question if available
            self.current_question += 1
            self.update_question()
        else:
            # Show the result page when the quiz is done
            self.phone_frame_quiz_view.visible = False
            self.phone_frame_result_view.visible = True
            if self.page:
                self.page.update()
            self.show_result()

    def previous_question(self, e):
        """Handle moving back to the previous question."""
        if self.current_question > 0:
            # Move back one question and remove last answer
            self.current_question -= 1
            self.answers.pop()
            # Update question view
            self.update_question()

    def show_result(self):
        global personality
        personality_scores = [sum(1 for a in self.answers if a == i) for i in range(3)]
        personality_index = personality_scores.index(max(personality_scores))
        personalities = ["Athena", "Hammer", "Felix"]
        personality = personalities[personality_index]

        # Header
        self.result_header.value = "Meet your very own gym buddy, coach, and trainer - all in one!"
        self.result_header.size = 28  # Increase font size
        self.result_header.weight = "bold"
        self.result_header.text_align = "center"

        # Wrap header in a container with padding
        header_container = ft.Container(
            content=self.result_header,
            padding=ft.padding.only(top=200),  # Increased top padding
            alignment=ft.alignment.center
        )

        # Image
        self.result_image.src = f"assets/{personality.lower()}_icon.png"
        self.result_image.width = 200
        self.result_image.height = 200
        self.result_image.fit = ft.ImageFit.CONTAIN

        # Descriptions for each personality
        descriptions = {
            "Athena": "Athena is your no-nonsense fitness coach! She's direct, motivating, and always ready to guide you towards your goals. With Athena, you'll get clear instructions and a structured plan to help you succeed and feel amazing.",
            "Hammer": "Get ready to crush your fitness goals with Hammer! He's your go-to buddy for discussing your goals and creating a plan that's all about you. Hammer believes in teamwork and open conversations to help you stay motivated and on track.",
            "Felix": "Meet Felix, your super cool fitness buddy! He's here to cheer you on and give you that extra push you need. Felix is all about helping you reach your goals with a smile, using a delegation style that lets you take charge of your fitness journey."
        }

        # Set the result description
        self.result_description.value = descriptions[personality]
        self.result_description.size = 16
        self.result_description.text_align = "center"

        # Hide quiz view and show result view
        self.phone_frame_quiz_view.visible = False
        self.phone_frame_result_view.visible = True  # Set result view to be visible.
        if self.page:
            self.page.update()

    def go_to_chat(self, e):
        """Transition to chat app with personality."""
        global personality
        if self.quiz_done_callback:
            self.quiz_done_callback(personality)
        else:
            print("Callback not set")

    def skip_quiz(self, e):
        """Handle skipping the quiz and showing results directly."""
        self.answers = [0] * len(self.questions)  # Provide a default answer set.
        self.phone_frame_quiz_view.visible = False
        self.show_result()
        if self.page:
            self.page.update()