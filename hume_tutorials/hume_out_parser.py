import json
from pprint import pprint


POSITIVE_EMOTIONS = {
    "Admiration": True,
    "Adoration": True,
    "Aesthetic Appreciation": True,
    "Amusement": True,
    "Awe": True,
    "Calmness": True,
    "Concentration": True,
    "Contentment": True,
    "Craving": True,
    "Desire": True,
    "Determination": True,
    "Ecstasy": True,
    "Enthusiasm": True,
    "Entrancement": True,
    "Excitement": True,
    "Gratitude": True,
    "Interest": True,
    "Joy": True,
    "Love": True,
    "Nostalgia": True,
    "Realization": True,
    "Relief": True,
    "Romance": True,
    "Satisfaction": True,
    "Surprise (positive)": True,
    "Sympathy": True,
    "Triumph": True,
}

NEGATIVE_EMOTIONS = {
    "Anger": True,
    "Annoyance": True,
    "Anxiety": True,
    "Awkwardness": True,
    "Boredom": True,
    "Confusion": True,
    "Contempt": True,
    "Disappointment": True,
    "Disgust": True,
    "Distress": True,
    "Doubt": True,
    "Embarrassment": True,
    "Empathic Pain": True,
    "Envy": True,
    "Fear": True,
    "Guilt": True,
    "Horror": True,
    "Pain": True,
    "Sadness": True,
    "Sarcasm": True,
    "Shame": True,
    "Surprise (negative)": True,
    "Tiredness": True,
}


class Hume_Data:
    def __init__(self, path_to_json):
        # self.raw_data = json.load(path_to_json)["results"]["predictions"] # Get every file analysis
        self.raw_data = self.read_json(path_to_json)

    def wrapper(self):
        data = self.get_average_emotions()
        negative_averages = self.get_top_n_emotions(data, NEGATIVE_EMOTIONS)
        positive_averages = self.get_top_n_emotions(data, POSITIVE_EMOTIONS)
        pprint(negative_averages)
        pprint(positive_averages)

    def read_json(self, path_to_json):
        with open(path_to_json) as f:
            return json.loads(f.read())[0]["results"]["predictions"]

    def get_top_n_emotions(
        self, parsed_data: dict, emotion_type: dict, top_n=3
    ) -> dict:
        """Parses segments of videos and returns a string of their top N emotions

        Parameters
        ----------
        parsed_data : dict
            data from function: get_average_emotions()
        top_n : int
            represents top n emotions

        Returns
        -------
        dict =
            {'0-5-Hume-input-video.mp4': [('Amusement', 0.5361335585514705),
                                        ('Interest', 0.5038713276386261),
                                        ('Joy', 0.49698808093865715)],
            '10-15-Hume-input-video.mp4': [('Amusement', 0.5422676205635071),
                                            ('Interest', 0.50926606853803),
                                            ('Joy', 0.47855714758237206)],
            '15-17.02-Hume-input-video.mp4': [('Joy', 0.8632936307362148),
                                            ('Amusement', 0.8348885178565979),
                                            ('Excitement', 0.5327329039573669)],
            '5-10-Hume-input-video.mp4': [('Amusement', 0.6442351480325063),
                                        ('Joy', 0.6116871337095896),
                                        ('Interest', 0.49974467356999713)]}
        """
        pprint(emotion_type)
        res = {}
        for k_file_segment, v_dict in parsed_data.items():
            v_dict_copy = {}
            for k_emotion_name, v_average in v_dict.items():
                if emotion_type.get(k_emotion_name, None):
                    v_dict_copy[k_emotion_name] = v_average

            sorted_items = sorted(
                v_dict_copy.items(), key=lambda item: item[1]["average"], reverse=True
            )
            top_emotions = sorted_items[:top_n]
            res[k_file_segment] = top_emotions
        return res

    def get_average_emotions(self) -> dict:
        """Emotion type takes in either POSITIVE_EMOTIONS or NEGATIVE_EMOTIONS"""

        def emotion_level(emotion_average: float) -> str:
            if 0 <= emotion_average < 0.4:
                return "none to slight "
            elif 0.4 <= emotion_average < 0.8:
                return ""
            else:
                return "overly "

        file_data = {}

        for idx, file in enumerate(self.raw_data):
            file_name = self.raw_data[idx]["file"]
            print(f"{file_name=}")

            grouped_predictions: list[dict] = self.raw_data[idx]["models"]["face"][
                "grouped_predictions"
            ][
                0
            ]  # each dict represents frames
            grouped_predictions = grouped_predictions["predictions"]
            num_frames = len(grouped_predictions)

            segment_emotion_data = {}
            for idx, frame in enumerate(grouped_predictions):
                emotions: list[dict] = frame["emotions"]

                for idx, emotion in enumerate(emotions):
                    emotion_name = emotion["name"]
                    emotion_score = emotion["score"]
                    if not segment_emotion_data.get(emotion_name, None):
                        segment_emotion_data[emotion_name] = emotion_score
                    else:
                        segment_emotion_data[emotion_name] += emotion_score

            for k_emotion, v_score in segment_emotion_data.items():
                if v_score == "":
                    continue
                average = v_score / num_frames
                segment_emotion_data[k_emotion] = {
                    "average": average,
                    "str_repr": f"{emotion_level(average)}{k_emotion}",
                }
            file_data[file_name] = segment_emotion_data
        return file_data


if __name__ == "__main__":
    # obj = Hume_Data("Sample-Outputs/sample-audio-and-face.json")
    obj = Hume_Data("predictions.json")
    obj.wrapper()
