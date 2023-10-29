from calhacks.state import State

import reflex as rx
import re


class ResultsState(State):
    """The app state."""
    # The images to show.
    videos: list[str]
    has_videos: bool = False
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
        self.has_videos = True
        # TODO: uncommend below to show results_view() component when video file is uploaded
        # self.is_uploaded = True
        

color = '' # TODO: make it pretty


def category_heading(text) -> rx.Component:
    return rx.heading(
        rx.span(
            text,
            display="content-block",
            padding=".1em .1em",
            border_radius="1000px",
            background="#BFDBF7"
        ),
        margin_top="16px",
        margin_bottom="16px"
    )

def video_and_report(video) -> rx.Component:
    return rx.card(
        rx.grid(
            rx.video(url=video),
            rx.box(
                category_heading("Content"),
                rx.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                category_heading("Presentation"),
                rx.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                category_heading("Key Moments"),
                rx.list(
                    rx.list_item("00:05 -- High Nervousness"),
                    rx.list_item("00:20 -- High Confidence"),
                    rx.list_item("03:40 -- High Rizz"),
                )
            ),
            grid_template_columns="1fr 1fr",
            align_items="center",
            gap="32px"
        )
    )


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
                rx.upload_files(),
            ),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files,
        ),
        rx.cond(
            ResultsState.has_videos,
            rx.flex(
                rx.foreach(
                    ResultsState.videos,
                    lambda video: video_and_report(video)
                ),
                background_color="#E1E5F2",
                flex_direction="column",
                padding="32px",
                gap="32px"
            ),
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
    