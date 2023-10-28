"""App explainer + setup permissions"""

import reflex as rx


def get_started() -> rx.Component:
    return rx.container(
        rx.text('Get Started Page')
    )