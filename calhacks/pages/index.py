"""The dashboard page."""

import reflex as rx

@rx.page(route="/")
def index() -> rx.Component:
    return rx.grid(
        rx.box(),
        rx.heading(
            rx.span(
                "IntervYou",
                display="content-block",
                padding=".1em .1em",
                border_radius="1000px",
                background="#BFDBF7"
            ),
            size="2xl",
            text_align="center"),
        rx.heading('AI-driven interview preparation for self-improvement', size="md", text_align="center"),
        rx.text('a project by Memory Leeks, Calhacks 10.0', text_align="center"),
        rx.center(
            rx.link(
                rx.button('Get Started', background="#BFDBF7"),
                href='http://localhost:3000/setup',
            ),
        ),
        rx.box(),
        bg='white',
        width='100dvw',
        height='100dvh',
        align_items="end",
        grid_template_rows='1fr 20% 10% 10% 20% 2fr'
    )