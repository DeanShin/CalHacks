"""Welcome to Reflex!."""

from calhacks import styles
from calhacks.pages import index, get_started

# Import all the pages.
from calhacks.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.add_page(index, '/')
app.compile()
