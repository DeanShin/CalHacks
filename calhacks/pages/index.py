"""The dashboard page."""

import reflex as rx

_debug = True
_debug_style='2px solid red' if _debug else ''

def top() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading('Project Name TBD'),
            rx.text('by Memory Leeks, Calhacks 10.0'),
            rx.text('Add quick project description'),
            border=_debug_style
        ),
        rx.link(
            rx.button('Get Started'),
            href='http://localhost:3000/setup'
        ),
        bg='white',
        border=_debug_style,
        width='100vw',
        height='100vh'
    )

@rx.page(route="/")
def index() -> rx.Component:
    return rx.container(
        top()
    )