"""
Demonstrating how to get prosody embeddings using Hume's Streaming API and Python SDK
https://dev.hume.ai/docs/streaming-api#understand-prosody-from-video-or-audio
"""
import asyncio
import json
from hume import HumeStreamClient, StreamSocket
from hume.models.config import ProsodyConfig, BurstConfig
API_KEY = "4yGVS4iJNNlcvRj08PLnyV9luGTQMG8Dz7YGDEFHzQlkkKA6"


async def main():
    # Initialize client connection
    client = HumeStreamClient(API_KEY)
    # Configure websocket
    # Defining ProsodyConfig allows Prosody analysis configuration
    configs = ProsodyConfig()
    # Create websocket connection
    async with client.connect([configs]) as socket:
        # Use socket connection to send file
        # result = await socket.send_file(r"C:\Users\megaw\Downloads\Hume-input-audio.mp3")
        # result = await socket.send_file(r"C:\Users\megaw\Downloads\short_clip.mp4")
        result = await socket.send_file(r"C:\Users\megaw\Downloads\audio_clip.mp3")
        #emotions = result["language"]["predictions"][0]["emotions"]
        #print(type(result))
        print(json.dumps(result, indent=4))
        #print(result)

asyncio.run(main())
