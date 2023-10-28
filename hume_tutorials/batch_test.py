from hume import HumeBatchClient
from hume.models.config import ProsodyConfig # State of speech
import os
import json
import requests

API_KEY = os.environ.get("API_KEY")

def first_test():
    url = "https://api.hume.ai/v0/batch/jobs"
    files = { "file": ("audio_clip.mp3", open("audio_clip.mp3", "rb"), "audio/mpeg") }
    payload = { "json": "{}" }
    headers = { 
            "accept": "application/json",
            "X-Hume-Api-Key": API_KEY
            }
    response = requests.post(url, data=payload, files=files, headers=headers)
    res = response.json()
    job_id = res["job_id"]
    print(job_id)


def test_methods():
    client = HumeBatchClient(API_KEY)
    file = ["audio_clip.mp3"]
    config = [ProsodyConfig()]
    job = client.submit_job([], config, files=file)

    print("Running...", job)

    job.await_complete()
    print(job.get_predictions())


test_methods()
#main()
