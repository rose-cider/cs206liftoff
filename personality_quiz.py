import flet as ft

class PersonalityQuiz:
    def __init__(self):
        self.questions = [
            "How would you describe your work ethic?",
            "Would a strict teacher motivate you to achieve your goals?",
            "How do you react to missing a workout?",
            "What motivates you to push through tough exercises?",
            "What kind of encouragement works best for you?",
            "What do you value most in a workout buddy?"
        ]
        self.options = [
            ["Methodical and steady.", "Decently productive but with the tendency to lose motivation...", "Unpredictable and spontaneous."],
            ["Yes! A little strictness is what I need to do my best.", "It makes me less motivated or maybe even annoyed...", "I need lots of firm guidance to get anything done."],
            ["I need a firm push to get back on track and not lose progress.", "I'd appreciate talking through what went wrong and adjusting the plan.", "I prefer reflecting on it myself and figuring out how to move forward."],
            ["A strict reminder of my goals and why I need to stick to the plan.", "A discussion on how the workout benefits me, so I stay engaged...", "The freedom to choose when and how I challenge myself."],
            ["A tough, no-nonsense approach that reminds me to stay focussed.", "Positive reinforcement and a conversation about my progress.", "Gentle suggestions and leaving me to motivate myself."],
            ["Someone who is firm and keeps me disciplined.", "Someone who can explain why we're doing certain exercises and listens to my feedback.", "Someone who lets me figure things out and offers support when I ask for it."]
        ]
        self.current_question = 0
        self.answers = []

    def main(self, page: ft.Page):
        page.title = "Personality Quiz"
        page.window_width = 390
        page.window_height = 844
        page.window_frameless = True

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

        # Quiz view layout
        self.quiz_view = ft.Column(
            [
                ft.Container(content=self.question_text, padding=ft.padding.only(top=150)),  # Padding for question text
                ft.Column(self.option_buttons, spacing=10),
                ft.Container(height=20),  # Spacer
                self.back_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )

        # Result view layout (hidden initially)
        self.result_text = ft.Text(
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER
        )

        self.next_button = ft.ElevatedButton(
            text="Next",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=50),
                padding=20  # Padding for internal spacing inside button
            ),
            bgcolor="#F1B04C",
            color="white",
            width=271,
        )

        self.result_view = ft.Column(
            [
                ft.Container(content=self.result_text, padding=ft.padding.only(top=100)),
                ft.Container(expand=True),  # Pushes next button to bottom
                self.next_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
            visible=False  # Hidden initially
        )

        page.add(ft.Column([self.quiz_view, self.result_view], expand=True))
        self.update_question()

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
            # Show result if all questions are answered
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
        """Calculate and display results."""
        personality_scores = [sum(1 for a in self.answers if a == i) for i in range(3)]
        
        # Determine personality type based on scores
        personality = ["Strict", "Balanced", "Relaxed"][personality_scores.index(max(personality_scores))]
        
        # Update result view content
        self.result_text.value = f"Your AI workout buddy personality: {personality}"
        
        # Switch views: hide quiz view, show result view
        self.quiz_view.visible = False
        self.result_view.visible = True
        
        # Update UI for result view
        self.result_view.update()

# Uncomment this line to run the app:
# ft.app(target=PersonalityQuiz().main)