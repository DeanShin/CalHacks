import os
import subprocess
from subprocess import DEVNULL

import speech_recognition as sr
from pydub import AudioSegment

current_directory = os.path.dirname(os.path.abspath(__file__))
AUDIO_OUT_DIR = os.path.join(current_directory, "Audio-Output")

if not os.path.exists(AUDIO_OUT_DIR):
    os.mkdir(AUDIO_OUT_DIR)


def convert_webm_to_mp4(webm: str, working_dir=None) -> None:
    mp4 = f"{webm.rstrip('.webm')}.mp4"

    try:
        # Use FFmpeg to convert MP4 or webm to WAV
        cmd = ["ffmpeg", "-i", webm, f"{AUDIO_OUT_DIR}/{mp4}", "-y"]
        subprocess.run(cmd, check=True, stdout=DEVNULL, stderr=DEVNULL)

        print(f"Conversion complete: {webm} -> {mp4}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting the file: {e}")
    except FileNotFoundError:
        print(
            "FFmpeg not found. Please install FFmpeg and make sure it's in your system's PATH."
        )


def convert_video_to_wav(mp4_or_webm: str, working_dir=None) -> None:
    wav_file = f"{mp4_or_webm.rstrip('-video.mp4').rstrip('.webm')}-audio.wav"

    try:
        # Use FFmpeg to convert MP4 or webm to WAV
        cmd = ["ffmpeg", "-i", mp4_or_webm, "-vn", f"{AUDIO_OUT_DIR}/{wav_file}", "-y"]
        subprocess.run(cmd, check=True, stdout=DEVNULL, stderr=DEVNULL)

        print(f"Conversion complete: {mp4_or_webm} -> {wav_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting the file: {e}")
    except FileNotFoundError:
        print(
            "FFmpeg not found. Please install FFmpeg and make sure it's in your system's PATH."
        )


def wav_to_audio_transcript() -> str:
    recognizer = sr.Recognizer()

    input_file = "Hume-input-audio.wav"

    with sr.AudioFile(input_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

        transcript = ""
        try:
            transcript = recognizer.recognize_google(audio)
            print("Transcript: " + transcript)

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")

        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))
    return transcript


if __name__ == "__main__":
    print(f"{current_directory=}")
    convert_video_to_wav("Hume-input-video.mp4")
    res = wav_to_audio_transcript()
    print(res)
