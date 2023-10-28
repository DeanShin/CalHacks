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
from moviepy.editor import *

current_directory = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(current_directory, "Output-Segments")


def split_input_to_segments(video_path: str, video_seg_len=5) -> None:
    # TODO might have strip path from video path
    video = VideoFileClip(video_path)
    duration = video.duration
    print(f"{duration=}")

    lower = 0
    upper = video_seg_len
    while upper < duration:
        subclip = video.subclip(lower, upper)
        subclip.write_videofile(f"{lower}-{upper}-{video_path}")
        lower += 5
        upper += 5

    upper -= 5
    subclip = video.subclip(upper, duration)
    subclip.write_videofile(f"{upper}-{duration}-{video_path}")


def _move_output(video_path) -> None:
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    pattern = r"\d+-[\d.]*-" + video_path
    res = re.search(pattern, f"10-15-{video_path}").group()
    segments = [
        re.search(pattern, p).group()
        for p in os.listdir(current_directory)
        if re.search(pattern, p)
    ]
    for i in segments:
        os.rename(i, os.path.join(OUTPUT_DIR, i))


if __name__ == "__main__":
    name = "Hume-input-video.mp4"
    split_input_to_segments(name)
    _move_output(name)
