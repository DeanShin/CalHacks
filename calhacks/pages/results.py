from calhacks.state import State

import reflex as rx

class ResultsState(State):
    """The app state."""
    # The images to show.
    img: list[str]
    is_uploaded: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).
        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
        is_uploaded = True

color = 'E1E5F2' # lightgrey

def upload_view() -> rx.Component:
    """The main view."""
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
            ),
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text)),
        rx.button(
            "Upload",
            on_click=lambda: ResultsState.handle_upload(
                rx.upload_files()
            ),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files,
        ),
        rx.foreach(
            ResultsState.img, lambda img: rx.image(src=img)
        ),
        padding="5em",
    )


def results_view() -> rx.Component:
    return rx.text('text')

@rx.page(route='/results')
def results():
    return rx.cond(
        ResultsState.is_uploaded,
        results_view(),
        upload_view()
    )