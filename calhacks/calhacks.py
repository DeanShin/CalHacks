"""Welcome to Reflex!."""

from calhacks import styles

# Import all the pages.
from calhacks.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
