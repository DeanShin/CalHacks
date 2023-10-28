import reflex as rx

from calhacks.state import State


class QuizState(State):
    questions = ['test 1', 'test 2', 'test 3']
    question_number: int = 0


    def next_question(self):
        # currently, we will only ask a single question
        return rx.call_script("window.location.href='/results'")


@rx.page()
def quiz():
    return rx.grid(
        rx.box(),
        rx.center(
            rx.heading(
                "fasdfjadsklfjdslkf asdjf asdjf lkasdjflkadsa fjklasf ldskafd",
                size="xl",
                text_align="center",
                max_width="60%"
            ),
        ),
        rx.center(
            rx.button(
                "Finish question",
                on_click=QuizState.next_question,
            ),
        ),
        rx.box(),
        width="100dvw",
        height="100dvh",
        align_items="center",
        grid_template_rows="1fr 40% 20% 1fr"
    )
