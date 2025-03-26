# personality_quiz.py
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
        page.title = "AI Personality Quiz"
        page.window_width = 390
        page.window_height = 844
        page.window_frameless = True

        # Fixed the question text initialization
        self.question_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)
        
        self.option_buttons = [ft.ElevatedButton(text=f"Option {i+1}", on_click=self.next_question) for i in range(3)]
        self.back_button = ft.ElevatedButton("Back", on_click=self.previous_question, visible=False)

        self.quiz_view = ft.Column(
            [self.question_text] + self.option_buttons + [self.back_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        )

        self.result_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
        self.restart_button = ft.ElevatedButton("Restart Quiz", on_click=self.restart_quiz)

        self.result_view = ft.Column(
            [self.result_text, self.restart_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            visible=False
        )

        page.add(ft.Column([self.quiz_view, self.result_view]))
        self.update_question()

    def update_question(self):
        self.question_text.value = self.questions[self.current_question]
        for i, button in enumerate(self.option_buttons):
            button.text = self.options[self.current_question][i]
        self.back_button.visible = self.current_question > 0
        self.quiz_view.update()

    def next_question(self, e):
        self.answers.append(self.option_buttons.index(e.control))
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.update_question()
        else:
            self.show_result()

    def previous_question(self, e):
        if self.current_question > 0:
            self.current_question -= 1
            self.answers.pop()
            self.update_question()

    def show_result(self):
        personality_scores = [sum(1 for a in self.answers if a == i) for i in range(3)]
        personality = ["Strict", "Balanced", "Relaxed"][personality_scores.index(max(personality_scores))]
        self.result_text.value = f"Your AI workout buddy personality: {personality}"
        self.quiz_view.visible = False
        self.result_view.visible = True
        self.result_view.update()

    def restart_quiz(self, e):
        self.current_question = 0
        self.answers = []
        self.quiz_view.visible = True
        self.result_view.visible = False
        self.update_question()

# ft.app(target=PersonalityQuiz().main)
