"""
This is a simple demonstration of Hume's Streaming API using Python SDK
"""
import asyncio

from hume import HumeStreamClient
from hume.models.config import LanguageConfig
API_KEY = "4yGVS4iJNNlcvRj08PLnyV9luGTQMG8Dz7YGDEFHzQlkkKA6"


samples = [
    "Mary had a little lamb,",
    "Its fleece was white as snow."
    "Everywhere the child went,"
    "The little lamb was sure to go."
        ]

async def main():
    # Initialize client connection
    client = HumeStreamClient(API_KEY)
    # Hume model config
    config = LanguageConfig()
    async with client.connect([config]) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            emotions = result["language"]["predictions"][0]["emotions"]
            print(emotions)

asyncio.run(main())
