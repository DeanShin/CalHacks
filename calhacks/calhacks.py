"""Welcome to Reflex!."""

from calhacks import styles
from calhacks.pages import index, setup

# Import all the pages.
from calhacks.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.add_page(index, route='/')
app.add_page(get_started, route='/get-started')
app.compile()
