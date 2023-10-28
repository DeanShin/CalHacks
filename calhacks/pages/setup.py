import reflex as rx

from calhacks.state import State


class SetupState(State):
    show_empty_context_error = False

    def update_interview_context(self, s):
        self.show_empty_context_error = False
        self.interview_context = s

    def on_pressed_ready(self):
        if len(self.interview_context) == 0:
            self.show_empty_context_error = True
            return
        return rx.call_script("navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(() => { window.location.href = '/quiz' })")


@rx.page()
def setup():
    return rx.grid(
        rx.heading("How it works", size="xl", text_align="center"),
        rx.grid(
            rx.card(
                rx.text(
                    "Get interview questions specifically asked in your industry for the most effective practice."),
                header=rx.heading(
                    "Fill out your industry", size="lg"
                ),
            ),
            rx.card(
                rx.text(
                    "Turn your camera on and practice answering the provided questions as if you were in an actual interview."),
                header=rx.heading(
                    "Practice your interview", size="lg"
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
                    "Interview context",
                ),
                rx.text_area(
                    on_change=SetupState.update_interview_context,
                    placeholder="I am applying for a position in Software Engineering as a new grad",
                    width="400px",
                    is_invalid=SetupState.show_empty_context_error
                )
            )
        ),
        rx.center(
            rx.button(
                rx.text("Get Started"),
                width="200px",
                on_click=SetupState.on_pressed_ready
            ),
        ),
        grid_template_rows = "200px auto 200px 100px",
        align_items = "center",
        justify_content = "center",
        margin = "32px",
    )