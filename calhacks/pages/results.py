from calhacks.state import State

import reflex as rx

class ResultsState(State):
    """The app state."""
    # The images to show.
    videos: list[str]
    is_uploaded: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        """
        Handle the upload video files and store it locally in .web/public directory.

        :param files: The uploaded files.
        """
        print('handling')
        for file in files:
            upload_data = await file.read()
            outfile = f".web/public/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the videos var.
            self.videos.append(file.filename)
        # TODO: uncommend below to show results_view() component when video file is uploaded
        # self.is_uploaded = True
        

color = '' # TODO: make it pretty

def upload_view() -> rx.Component:
    """
    Have user drag or upload .webm files.
    videos are stored in ./web/public folder
    """
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
            accept={
                'video/webm': ['.webm']
            },
            border=f"2px dotted {color}",
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
            ResultsState.videos, lambda videos: rx.box(rx.heading('video!'), rx.video(url=videos))
        ),
        padding="5em",
    )


def results_view() -> rx.Component:
    """Generate results after videos are uploaded"""
    return rx.text('text')


@rx.page(route='/results')
def results():
    return rx.cond(
        ResultsState.is_uploaded,
        results_view(),
        upload_view()
    )
    