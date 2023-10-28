import reflex as rx

from calhacks.state import State


class SetupState(State):
    def on_pressed_ready(self):
        return rx.call_script("navigator.getUserMedia({ video: true, audio: true }, "
                              "() => { window.location.href = '/' }, "
                              "() => { window.location.href = '/ })")

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
            rx.button(
                rx.text("Get Started"),
                width="200px",
                on_click=lambda : SetupState.on_pressed_ready
            ),
        ),
        grid_template_rows = "200px auto 200px",
        align_items = "center",
        justify_content = "center",
        margin = "32px",
    )