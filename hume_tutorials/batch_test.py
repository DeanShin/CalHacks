from hume import HumeBatchClient
from hume.models.config import ProsodyConfig # State of speech
from hume.models.config import FaceConfig # Facial expression
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


def multi_test_method():
    client = HumeBatchClient(API_KEY)
    filepaths = ["clips.zip"]
    config = [FaceConfig(identify_faces=True), ProsodyConfig()]
    job = client.submit_job([], config, files=filepaths)

    print("Running...", job)

    job.await_complete()
    print(job.get_predictions())

    print("Saving predictions to predictions.json")
    job.download_predictions("predictions.json")

    print("Artifacts download to artifacts.zip")
    job.download_artifacts("artifacts.zip")


def single_test_method():
    client = HumeBatchClient(API_KEY)
    file = ["audio_clip.mp3"]
    config = [ProsodyConfig()]
    job = client.submit_job([], config, files=file)

    print("Running...", job)

    job.await_complete()
    #print(job.get_predictions())
    print("Saving predictions to speech_pred.json")
    job.download_predictions("speech_pred.json")

    print("Artifacts download to speech_artifacts.zip")
    job.download_artifacts("speech_artifacts.zip")


def check_job():
    client = HumeBatchClient(API_KEY)
    job = client.get_job('a6006ada-3ae0-4c18-9792-af0e2be5cbd5')
    status = job.get_status()
    print(status)



#multi_test_method()
single_test_method()
#main()
#check_job()
