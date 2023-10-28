from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig
API_KEY = "4yGVS4iJNNlcvRj08PLnyV9luGTQMG8Dz7YGDEFHzQlkkKA6"

client = HumeBatchClient(API_KEY)
urls = ["https://storage.googleapis.com/hume-test-data/video/armisen-clip.mp4"]
configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
predictions = job.get_predictions()
print(predictions)
#print("Predictions downloaded to predictions.json")
