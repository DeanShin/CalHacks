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


def multithreaded_segmenting_wrapper(video_path: str) -> dict[tuple, str]:
    """Processes segments of videos, returns bounds for easy mapping

    Parameters
    ----------
    video_path : str
        path to input video file

    Returns
    -------
    dict[tuple,str]
        returns a diction of bounds tuple(int, int) mapped to
        path. Will make mapping out hume output easier

    {(0, 5): 'path/to/Output-Segments/0-5-Hume-input-video.mp4',
    (5, 10): 'path/to/Output-Segments/5-10-Hume-input-video.mp4',
    ...
    }
    Examples
    --------
    FIXME: Add docs.
    _ = multithreaded_segmenting_wrapper([video_path])   # to disregard output
    res = multithreaded_segmenting_wrapper([video_path]) # to use output

    """
    obj = Video(video_path)
    bounds = obj.get_bounds()

    num_processes = os.cpu_count()
    pool = Pool(processes=num_processes)

    process_segment_partial = partial(process_segment, video_path=name)
    pool.map(process_segment_partial, bounds)

    pool.close()
    pool.join()

    move_output(name)

    return get_bound_and_file_dict(bounds)


def get_bound_and_file_dict(
    bounds: list[tuple], output_dir=OUTPUT_DIR
) -> dict[tuple, str]:
    res: dict[tuple, str] = {}
    files = os.listdir(output_dir)
    for lower, upper in bounds:
        for f_ in files:
            if str(lower) in f_ and str(upper) in f_:
                res[(lower, upper)] = os.path.join(output_dir, f_)
    return res


def zip_output_folder(folder_to_archive=OUTPUT_DIR) -> None:
    hume_dir_name = "hume-input"
    hume_dir = os.path.join(current_directory, hume_dir_name)
    if not os.path.exists(hume_dir):
        os.mkdir(hume_dir)

    shutil.make_archive(hume_dir_name, "zip", folder_to_archive)
    try:
        shutil.move(f"{hume_dir_name}.zip", hume_dir)
    except Exception as e:
        print()
        print(e)
        print()

if __name__ == "__main__":
    from pprint import pprint

    name = "Hume-input-video.mp4"
    res = multithreaded_segmenting_wrapper(name)

    print()
    print("======================================")
    pprint(res)
    print("======================================")
    print("^^^ Raw Data that will be used for our future analysis")
    print()

    print("======================================")
    print(f"Zipping out from {OUTPUT_DIR=} to {current_directory}/Hume-input/hume-input.zip")
    zip_output_folder()
    print("======================================")

