from calhacks.state import State
from calhacks.hume.hume_out_parser import Hume_Data
from typing import List, Tuple

import reflex as rx
import re
import asyncio

from ..hume import dean_test_data

class ResultsState(State):
    """The app state."""
    # The images to show.
    videos: list[str]
    video_to_question_number: dict[str, int]
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
            self.video_to_question_number[file.filename] = int(re.search(r'[\d]+', file.filename).group(0))
            self.video_data[file.filename] = (None, [], [])
        self.has_videos = True
        return ResultsState.populate_video_data

    async def set_content(self, file):
        await asyncio.sleep(3)
        async with self:
            self.video_data[file.filename] = (
                dean_test_data.get_dean_set_content(),
                self.video_data[file.filename][1],
                self.video_data[file.filename][2]
            )


    async def set_top_emotions(self, file):
        await asyncio.sleep(3.1)
        async with self:
            self.video_data[file.filename] = (
                self.video_data[file.filename][0],
                dean_test_data.get_dean_top_emotions(),
                self.video_data[file.filename][2]
            )
            


    async def set_key_moments(self, file):
        # TODO: get video from self.videos, get hume data and parse with hume_parser
        hume_parser = Hume_Data()
        await hume_parser.parse()
        await asyncio.run()
        high_emotions: list = hume_parser.top_highs
        print(high_emotions)
        async with self:
            self.video_data[file.filename] = (
                self.video_data[file.filename][0],
                self.video_data[file.filename][1],
                [
                    # ["00:33", "High Nervousness"],
                    # ["00:40", "High Rizz"],
                    # ["01:23", "High Confidence"],
                    [high_emotions[0][1]['timestamp'], high_emotions[0][1]['str_repor']]
                    [high_emotions[1][1]['timestamp'], high_emotions[1][1]['str_repor']]
                    [high_emotions[2][1]['timestamp'], high_emotions[2][1]['str_repor']]
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
        rx.box(
            rx.cond(
                ResultsState.video_to_question_number[video] is not None,
                rx.heading(State.questions[ResultsState.video_to_question_number[video]], margin_bottom='16px'),
            ),
            rx.grid(
                rx.video(url=f'/{video}'),
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
                                lambda v: rx.text(v)
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
    
