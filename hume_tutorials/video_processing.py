# Preliminary Steps
# 1. Import Video with Audio
# 2. Split into 5 second increments 
# 3. Detach audio from these 5 second clips
#    1. result would be 5 second video and audio clips that we can leverage both apis
# 4. Create a map of the timestamps using these clips
# 5. For every 5 second clip
#    1. Send audio and video to hume
#       1. Can we send a zip file of all 5 second clips to hume?
#    2. return result
#    3. map results to time-span (ex: 0:00 - 0:05)
# 6. Deduce "spikes" in emotions
import os
import re
import shutil

from multiprocessing import Pool
from moviepy.editor import *
from functools import partial

current_directory = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(current_directory, "Output-Segments")


class Video:
    def __init__(self, path: str) -> None:
        self.video = VideoFileClip(path)
        self.path = path

    def get_bounds(self, video_seg_len=5) -> list[tuple]:
        duration = self.video.duration

        lower = 0
        upper = video_seg_len
        bounds: list[tuple] = []
        while upper < duration:
            bounds.append((lower, upper))
            lower += 5
            upper += 5

        upper -= 5
        bounds.append((upper, duration))
        return bounds

    def split_input_to_segments(self, segment: tuple[int | float]) -> None:
        lower, upper = segment
        subclip = self.video.subclip(lower, upper)
        subclip.write_videofile(f"{lower}-{upper}-{self.path}")


def process_segment(segment, video_path):
    video = Video(video_path)
    video.split_input_to_segments(segment)


def move_output(video_path, out_dir=OUTPUT_DIR) -> None:
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    pattern = r"\d+-[\d.]*-" + video_path
    segments = [
        re.search(pattern, p).group()
        for p in os.listdir(current_directory)
        if re.search(pattern, p)
    ]
    for i in segments:
        shutil.move(i, os.path.join(out_dir, i))


def multithreaded_segmenting_wrapper(video_path: str) -> None:
    obj = Video(video_path)
    bounds = obj.get_bounds()

    num_processes = os.cpu_count()
    pool = Pool(processes=num_processes)

    process_segment_partial = partial(process_segment, video_path=name)
    pool.map(process_segment_partial, bounds)

    pool.close()
    pool.join()

    move_output(name)


if __name__ == "__main__":
    name = "Hume-input-video.mp4"
    multithreaded_segmenting_wrapper(name)
