from calhacks.state import State
from typing import List, Tuple

import reflex as rx
import re
import asyncio

class ResultsState(State):
    """The app state."""
    # The images to show.
    videos: list[str]
    has_videos: bool = False
    is_uploaded: bool = False
    _files: List[rx.UploadFile]
    video_data: dict[str, Tuple[str, List[str], List[str]]] = {}

    @rx.background
    async def populate_video_data(self):
        for file in self._files:
            await asyncio.gather(
                self.set_content(file),
                self.set_top_emotions(file),
                self.set_key_moments(file)
            )

    async def handle_upload(self, files: List[rx.UploadFile]):
        """
        Handle the upload video files and store it locally in .web/public directory.

        :param files: The uploaded files.
        """
        self._files = files
        for file in files:
            upload_data = await file.read()
            outfile = f".web/public/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the videos var.
            self.videos.append(file.filename)
            self.video_data[file.filename] = (None, [], [])
        self.has_videos = True
        return ResultsState.populate_video_data

    async def set_content(self, file):
        await asyncio.sleep(3)
        async with self:
            self.video_data[file.filename] = (
                "Here is the content string Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                self.video_data[file.filename][1],
                self.video_data[file.filename][2]
            )

    async def set_top_emotions(self, file):
        await asyncio.sleep(3.1)
        async with self:
            self.video_data[file.filename] = (
                self.video_data[file.filename][0],
                ["Happiness", "Sadness", "Melancholy"],
                self.video_data[file.filename][2]
            )


    async def set_key_moments(self, file):
        await asyncio.sleep(3)
        async with self:
            self.video_data[file.filename] = (
                self.video_data[file.filename][0],
                self.video_data[file.filename][1],
                [
                    "00:33 -- High Nervousness",
                    "00:40 -- High Rizz",
                    "01:23 -- High Confidence",
                ]
            )



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
                rx.cond(
                    ResultsState.video_data[video][0],
                    rx.text('' if ResultsState.video_data[video][0] is None else ResultsState.video_data[video][0]),
                    rx.spinner()
                ),
                category_heading("Top Emotions"),
                rx.cond(
                    ResultsState.video_data[video][1],
                    rx.list(
                        rx.foreach(
                            ResultsState.video_data[video][1],
                            lambda v: rx.text(v)
                        )
                    ),
                    rx.spinner()
                ),
                category_heading("Key Moments"),
                rx.cond(
                    ResultsState.video_data[video][2],
                    rx.list(
                        rx.foreach(
                            ResultsState.video_data[video][2],
                            lambda v : rx.text(v)
                        )
                    ),
                    rx.spinner()
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
        padding="5em",
    )


def results_view() -> rx.Component:
    """Generate results after videos are uploaded"""
    return rx.flex(
        rx.foreach(
            ResultsState.videos,
            lambda video: video_and_report(video)
        ),
        background_color="#E1E5F2",
        flex_direction="column",
        padding="32px",
        gap="32px"
    )


@rx.page(route='/results')
def results():
    return rx.cond(
        ResultsState.has_videos,
        results_view(),
        upload_view()
    )
    