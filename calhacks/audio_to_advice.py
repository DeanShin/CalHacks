"""This file will take in a webp audio file, process it, build and send a gpt query, and save the response
"""
# TODO: async something to work with Dean's results.py
from gpt-clint import ChatGPT
from audio_processing.py import convert_video_to_wav, wav_to_audio_transcript
import asyncio

def main(question: str, file: str): -> str

    # process file
    audio_processor = Video()
    audio_processor.convert_video_to_wav(file)
    transcript = audio_processor.wav_to_audio_transcript(file)

    # make gpt client instance
    gpt = ChatGPT(question, transcript)
    asyncio.run(gpt.get_advice())
    return gpt.advice
