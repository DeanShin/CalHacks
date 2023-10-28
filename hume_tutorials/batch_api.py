from hume import HumeBatchClient
from hume.models.config import FaceConfig
import json
API_KEY = "4yGVS4iJNNlcvRj08PLnyV9luGTQMG8Dz7YGDEFHzQlkkKA6"

client = HumeBatchClient(API_KEY)
# Remote example data
# urls = ["https://hume-tutorials.s3.amazonaws.com/faces.zip"]
# Local video
filepaths = [ r"C:\Users\megaw\Downloads\vid_test.zip"]
config = FaceConfig()
# Remote example data
# job = client.submit_job(urls, [config])
# Local video
job = client.submit_job(None, [config], files=filepaths)

print(job)
print("Running...")

details = job.await_complete()
results = job.get_predictions()
print(results)
#job.download_predictions("video_predictions.json")
#print("Predictions downloaded to video_predictions.json")
