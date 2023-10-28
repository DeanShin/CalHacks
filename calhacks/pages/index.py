"""The dashboard page."""

import reflex as rx

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading('Project Name TBD'),
            rx.text('by Memory Leeks, Calhacks 10.0'),
            rx.text('Add quick project description')
        )
    )