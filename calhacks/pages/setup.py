import random

import reflex as rx

from calhacks.state import State
from calhacks.questions import role_to_questions


class SetupState(State):
    show_empty_context_error = False

    def update_interview_context(self, s):
        self.show_empty_context_error = False
        self.interview_context = s
        self.questions = random.sample(role_to_questions[self.interview_context], 3)

    def on_pressed_ready(self):
        if len(self.interview_context) == 0:
            self.show_empty_context_error = True
            return
        return rx.call_script("navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(() => { window.location.href = '/quiz' })")


@rx.page()
def setup():
    return rx.grid(
        rx.box(),
        rx.heading(
            rx.span(
                "How it works",
                display="content-block",
                padding=".1em .1em",
                border_radius="1000px",
                background="#BFDBF7"
            ),
            size="xl",
            text_align="center"
        ),
        rx.grid(
            rx.card(
                rx.text(
                    "Get interview questions specifically asked in your industry."),
                header=rx.heading(
                    "Choose your industry", size="lg"
                ),
            ),
            rx.card(
                rx.text(
                    "Turn your camera on and practice answering the provided questions as if you were in an actual interview."),
                header=rx.heading(
                    "Practice", size="lg"
                )
            ),
            rx.card(
                rx.text("Using state-of-the-art machine learning models, we'll generate a report outlining how you "
                        "did and give you advice on how to improve for your next interview!"),
                header=rx.heading(
                    "Review your results", size="lg"
                )
            ),
            grid_template_columns = "1fr 1fr 1fr",
            gap="16px",
            background_color="#E1E5F2",
            padding="16px"
        ),
        rx.center(
            rx.box(
                rx.text(
                    "Role",
                ),
                rx.select(
                    [*role_to_questions.keys()],
                    placeholder="Select the role that you are applying for",
                    on_change=SetupState.update_interview_context
                )
            )
        ),
        rx.center(
            rx.button(
                rx.text("Start the Interview"),
                width="200px",
                on_click=SetupState.on_pressed_ready,
                background="#BFDBF7"
            ),
        ),
        rx.box(),
        grid_template_rows = "1fr 3fr 5fr 1fr 1fr 1fr",
        align_items = "center",
        justify_content = "center",
        padding="32px",
        height="100dvh"
    )