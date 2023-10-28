import json
from pprint import pprint


class Hume_Data:
    def __init__(self, path_to_json):
        # self.raw_data = json.load(path_to_json)["results"]["predictions"] # Get every file analysis
        self.raw_data = self.read_json(path_to_json)

    def wrapper(self):
        file_data = {}

        for idx, file in enumerate(self.raw_data):
            file_name = self.raw_data[idx]["file"] 
            print(f"{file_name=}")

            grouped_predictions:list[dict] = self.raw_data[idx]["models"]["face"]["grouped_predictions"][0] # each dict represents frames
            grouped_predictions = grouped_predictions["predictions"]
            num_frames = len(grouped_predictions)

            emotion_data = {}
            for idx, frame in enumerate(grouped_predictions):
                emotions: list[dict] = frame["emotions"]

                for idx, emotion in enumerate(emotions):
                    emotion_name = emotion["name"]
                    emotion_score = emotion["score"]
                    if not emotion_data.get(emotion_name, None):
                        emotion_data[emotion_name] = emotion_score
                    else:
                        emotion_data[emotion_name] += emotion_score

            pprint(emotion_data)
            for k_emotion, v_score in emotion_data.items():
                average = v_score / num_frames
                emotion_data[k_emotion] = average
            break

            # file_data[file_name] = emotions
        # pprint(file_data)


    def read_json(self, path_to_json):
        with open(path_to_json) as f:
            return json.loads(f.read())[0]["results"]["predictions"]

    def get_emotions() -> dict:
        ...



if __name__ == "__main__":
    obj = Hume_Data("Sample-Outputs/sample-audio-and-face.json")
    obj.wrapper()
