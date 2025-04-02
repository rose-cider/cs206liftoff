# import flet as ft

# def render_quiz(page: ft.Page, quiz_done_callback=None):
#     page.views.clear()
#     page.title = "Personality Quiz"
#     page.padding = 0
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.bgcolor = "#1A1A1A"

#     # Quiz state
#     current_question = 0
#     answers = []
#     personality = None

#     questions = [
#             "How would you describe your work ethic?",
#             "Would a strict teacher motivate you to achieve your goals?",
#             "How do you react to missing a workout?",
#             "What motivates you to push through tough exercises?",
#             "What do you value most in a workout buddy?"
#     ]

#     options = [
#             ["Methodical and steady.", "Decently productive but with the tendency to lose motivation...", "Unpredictable and spontaneous."],
#             ["Yes! A little strictness is what I need to do my best.", "It makes me less motivated or maybe even annoyed...", "I need lots of firm guidance to get anything done."],
#             ["I need a firm push to get back on track and not lose progress.", "I'd appreciate talking through what went wrong and adjusting the plan.", "I prefer reflecting on it myself and figuring out how to move forward."],
#             ["A strict reminder of my goals and why I need to stick to the plan.", "A discussion on how the workout benefits me, so I stay engaged...", "The freedom to choose myself."],
#             ["A tough, no-nonsense approach that reminds me to stay focussed.", "Positive reinforcement and a conversation about my progress.", "Gentle suggestions and leaving me to motivate myself."],
#             ["Someone who is firm and keeps me disciplined.", "Someone who can explain why we're doing certain exercises and listens to my feedback.", "Someone who lets me figure things out!"]]

#     # Header with back button
#     header = ft.Container(
#         content=ft.Row([
#             ft.IconButton(
#                 icon=ft.icons.ARROW_BACK,
#                 on_click=lambda e: go_back(),
#                 icon_color=ft.colors.BLACK
#             ),
#             ft.Text("Personality Quiz", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
#             ft.TextButton("Skip", on_click=lambda e: skip_quiz())
#         ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#         padding=ft.padding.only(bottom=10)
#     )

#     # Dynamic content area
#     content_area = ft.Container(
#         alignment=ft.alignment.center,
#         expand=True
#     )

#     def update_question():
#         nonlocal current_question
#         question_text.value = questions[current_question]
        
#         option_buttons.controls = [
#             ft.ElevatedButton(
#                 text=options[current_question][i],
#                 style=ft.ButtonStyle(
#                     shape=ft.RoundedRectangleBorder(radius=14),
#                     padding=20,
#                     bgcolor="#FFA726",
#                     color="white"
#                 ),
#                 width=350,
#                 on_click=lambda e, i=i: answer_question(i)
#             ) for i in range(3)
#         ]
        
#         back_button.visible = current_question > 0
#         page.update()

#     def answer_question(option_idx):
#         nonlocal current_question, answers
#         answers.append(option_idx)
        
#         if current_question < len(questions) - 1:
#             current_question += 1
#             update_question()
#         else:
#             show_result()

#     def go_back():
#         nonlocal current_question, answers
#         if current_question > 0:
#             current_question -= 1
#             answers.pop()
#             update_question()

#     def skip_quiz():
#         nonlocal answers
#         answers = [0] * len(questions)  # Default answers
#         show_result()

#     def show_result():
#         nonlocal personality
#         # Calculate result
#         personality_scores = [answers.count(i) for i in range(3)]
#         personality_index = personality_scores.index(max(personality_scores))
#         personality = ["Athena", "Hammer", "Felix"][personality_index]
        
#         # Update UI for results
#         header.content.controls[2].visible = False  # Hide skip button
        
#         result_content = ft.Column([
#             ft.Text("Meet your gym buddy!", size=28, weight="bold", text_align="center"),
#             ft.Image(
#                 src=f"assets/{personality.lower()}_icon.png",
#                 width=200,
#                 height=200,
#                 fit=ft.ImageFit.CONTAIN
#             ),
#             ft.Text(
#                 get_personality_description(personality),
#                 size=16,
#                 text_align="center"
#             ),
#             ft.ElevatedButton(
#                 "Continue",
#                 style=ft.ButtonStyle(
#                     shape=ft.RoundedRectangleBorder(radius=50),
#                     padding=20,
#                     bgcolor="#F1B04C",
#                     color="white"
#                 ),
#                 width=271,
#                 on_click=lambda e: finish_quiz()
#             )
#         ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        
#         content_area.content = result_content
#         page.update()

#     def get_personality_description(personality):
#         descriptions = {
#             "Athena": "Your no-nonsense fitness coach! Clear instructions and structured plans.",
#             "Hammer": "Your goal-crushing buddy! Teamwork and open conversations.",
#             "Felix": "Your cheerful fitness buddy! Encouragement and flexibility."
#         }
#         return descriptions[personality]

#     def finish_quiz():
#         if quiz_done_callback:
#             quiz_done_callback(personality)
#         else:
#             page.go("/")  # Fallback navigation

#     # Initial welcome screen
#     welcome_content = ft.Column([
#         ft.Text("Welcome to LiftOff!", size=24, weight="bold", text_align="center"),
#         ft.Text(
#             "Let's find your perfect gym buddy with a quick personality quiz.",
#             size=16,
#             text_align="center"
#         ),
#         ft.ElevatedButton(
#             "Start Quiz",
#             style=ft.ButtonStyle(
#                 shape=ft.RoundedRectangleBorder(radius=50),
#                 bgcolor="#F1B04C",
#                 color="white"
#             ),
#             width=271,
#             on_click=lambda e: start_quiz()
#         )
#     ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

#     def start_quiz():
#         content_area.content = ft.Column([
#             ft.Container(ft.Text(questions[0], size=20, weight="bold", text_align="center")), 
#             option_buttons,
#             back_button
#         ], spacing=20)
#         update_question()

#     # Question UI components
#     question_text = ft.Text(size=20, weight="bold", text_align="center")
#     option_buttons = ft.Column(spacing=10)
#     back_button = ft.ElevatedButton(
#         "Back",
#         visible=False,
#         style=ft.ButtonStyle(
#             shape=ft.RoundedRectangleBorder(radius=50),
#             bgcolor="#F1B04C",
#             color="white"
#         ),
#         width=271,
#         on_click=lambda e: go_back()
#     )

#     # Initial content
#     content_area.content = welcome_content

#     # Phone frame layout
#     phone_frame = ft.Container(
#         content=ft.Column([
#             header,
#             content_area
#         ], spacing=0, expand=True),
#         width=390,
#         height=844,
#         bgcolor=ft.colors.WHITE,
#         border_radius=20,
#         border=ft.border.all(2, ft.colors.GREY_300),
#         padding=ft.padding.symmetric(horizontal=20, vertical=30)
#     )

#     page.views.append(ft.View("/quiz", [phone_frame]))
#     page.update()

import flet as ft

def render_quiz(page: ft.Page, quiz_done_callback=None):
    page.views.clear()
    page.title = "Personality Quiz"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#1A1A1A"

    # Quiz state
    current_question = 0
    answers = []
    personality = None

    questions = [
        "How would you describe your work ethic?",
        "Would a strict teacher motivate you to achieve your goals?",
        "How do you react to missing a workout?",
        "What motivates you to push through tough exercises?",
        "What do you value most in a workout buddy?"
    ]

    options = [
        ["Methodical and steady.", "Decently productive but with the tendency to lose motivation...", "Unpredictable and spontaneous."],
        ["Yes! A little strictness is what I need to do my best.", "It makes me less motivated or maybe even annoyed...", "I need lots of firm guidance to get anything done."],
        ["I need a firm push to get back on track and not lose progress.", "I'd appreciate talking through what went wrong and adjusting the plan.", "I prefer reflecting on it myself and figuring out how to move forward."],
        ["A strict reminder of my goals and why I need to stick to the plan.", "A discussion on how the workout benefits me, so I stay engaged...", "The freedom to choose myself."],
        ["A tough, no-nonsense approach that reminds me to stay focussed.", "Positive reinforcement and a conversation about my progress.", "Gentle suggestions and leaving me to motivate myself."]
    ]

    # Header with back button
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: go_back(),
                    icon_color=ft.colors.BLACK,
                ),
                ft.Text(
                    "Personality Quiz",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK,
                ),
                ft.TextButton(
                    "Skip",
                    on_click=lambda e: skip_quiz(),
                    style=ft.ButtonStyle(color=ft.colors.BLUE),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=20),  # Add horizontal padding
        height=60,  # Fixed height for header
    )

    # Dynamic content area
    content_area = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.padding.only(top=50),  # Push content down by 50 pixels
    )

    def update_question():
        nonlocal current_question
        question_text.value = questions[current_question]

        option_buttons.controls = [
            ft.ElevatedButton(
                text=options[current_question][i],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=20,
                    bgcolor="#FFA726",
                    color="white",
                ),
                width=350,
                on_click=lambda e, i=i: answer_question(i),
            )
            for i in range(3)
        ]

        back_button.visible = current_question > 0
        page.update()

    def answer_question(option_idx):
        nonlocal current_question, answers
        answers.append(option_idx)

        if current_question < len(questions) - 1:
            current_question += 1
            update_question()
        else:
            show_result()

    def go_back():
        nonlocal current_question, answers
        if current_question > 0:
            current_question -= 1
            answers.pop()
            update_question()

    def skip_quiz():
        nonlocal answers
        answers = [0] * len(questions)  # Default answers
        show_result()

    def show_result():
        nonlocal personality
        # Calculate result
        personality_scores = [answers.count(i) for i in range(3)]
        personality_index = personality_scores.index(max(personality_scores))
        personality = ["Athena", "Hammer", "Felix"][personality_index]

        # Update UI for results
        header.content.controls[2].visible = False  # Hide skip button

        result_content = ft.Column(
            [
                ft.Text("Meet your gym buddy!", size=28, weight="bold", text_align="center"),
                ft.Image(
                    src=f"assets/{personality.lower()}_icon.png",
                    width=200,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text(
                    get_personality_description(personality),
                    size=16,
                    text_align="center",
                ),
                ft.ElevatedButton(
                    "Continue",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=50),
                        padding=20,
                        bgcolor="#F1B04C",
                        color="white",
                    ),
                    width=271,
                    on_click=lambda e: finish_quiz(),
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment="center",  # Ensure horizontal centering of all elements
        )

        content_area.content = result_content
        page.update()

    def get_personality_description(personality):
        descriptions = {
            "Athena": "Athena is your no-nonsense fitness coach! She's direct, motivating, and always ready to guide you towards your goals. With Athena, you'll get clear instructions and a structured plan to help you succeed and feel amazing.",
            "Hammer": "Get ready to crush your fitness goals with Hammer! He's your go-to buddy for discussing your goals and creating a plan that's all about you. Hammer believes in teamwork and open conversations to help you stay motivated and on track.",
            "Felix": "Meet Felix, your super cool fitness buddy! He's here to cheer you on and give you that extra push you need. Felix is all about helping you reach your goals with a smile, using a delegation style that lets you take charge of your fitness journey."
        }
        return descriptions[personality]

    def finish_quiz():
        if quiz_done_callback:
            quiz_done_callback(personality)
        else:
            page.go("/")  # Fallback navigation

    # Initial welcome screen
    welcome_content = ft.Column(
        [
            ft.Text("We're exhilarated that you've joined us!", size=24, weight="bold", text_align="center"),
            ft.Text(
                "But before we start, we need to understand you better. Let's do a short personality quiz that will determine the best LiftOff gym buddy for you. For each of these questions, pick the answer that most closely resembles you.",
                size=16,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Row(  # Use Row to center the button
                [
                    ft.ElevatedButton(
                        "OK!",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=50),
                            bgcolor="#F1B04C",
                            color="white",
                        ),
                        width=271,
                        on_click=lambda e: start_quiz(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Center the button horizontally
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,  # Center elements vertically within column
    )



    def start_quiz():
        content_area.content = ft.Column(
            [
                ft.Container(ft.Text(questions[0], size=20, weight="bold", text_align="center")),
                option_buttons,
                back_button,
            ],
            spacing=20,
            alignment="center",  # Ensure vertical centering of content
            horizontal_alignment="center",  # Ensure horizontal centering of content
        )
        update_question()

    # Question UI components
    question_text = ft.Text(size=20, weight="bold", text_align="center")
    option_buttons = ft.Column(spacing=10)
    back_button = ft.ElevatedButton(
        "Back",
        visible=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=50),
            bgcolor="#F1B04C",
            color="white",
        ),
        width=271,
        on_click=lambda e: go_back(),
    )

    # Initial content
    content_area.content = welcome_content

    # Phone frame layout
    phone_frame = ft.Container(
        content=ft.Column([header, content_area], spacing=0, expand=True),
        width=390,
        height=844,
        bgcolor="#FFFFFF",
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_300),
    )

    page.views.append(ft.View("/quiz", [phone_frame]))
    page.update()
