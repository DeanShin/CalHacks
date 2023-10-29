"""The dashboard page."""

import reflex as rx

@rx.page(route="/")
def index() -> rx.Component:
    return rx.grid(
        rx.box(),
        rx.heading('IntervYou', size="2xl", text_align="center"),
        rx.heading('AI-driven interview preparation for self-improvement', size="md", text_align="center"),
        rx.text('a project by Memory Leeks, Calhacks 10.0', text_align="center"),
        rx.center(
            rx.link(
                rx.button('Get Started'),
                href='http://localhost:3000/setup'
            ),
        ),
        rx.box(),
        bg='white',
        width='100dvw',
        height='100dvh',
        align_items='center',
        justify_content='center',
        grid_template_rows='1fr 30% 20% 10% 20% 1fr'
    )