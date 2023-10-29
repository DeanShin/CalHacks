"""Hume data parser"""
import json
from pprint import pprint
import os
import os

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
    def __init__(self, path_to_json=os.path.join(os.path.abspath(__file__),'/../hume/outputs/predictions.json')):

        # TODO: find relative path to json from repo
        # self.raw_data = json.load(path_to_json)["results"]["predictions"] # Get every file analysis
        self.raw_data = self.read_json('./calhacks/hume/outputs/predictions.json')
        self.negative_averages = []
        self.positive_averages = []
        self.top_highs = []

    def parse(self):
        avg_data, high_data = self.parse_avg_and_high_emotions()
        # TODO: get top 3 average overall regardless of emotion type?
        self.negative_averages = self.get_top_n_emotions(avg_data, NEGATIVE_EMOTIONS)
        self.positive_averages = self.get_top_n_emotions(avg_data, POSITIVE_EMOTIONS)
        self.top_highs = self.get_top_n_high_emotions(high_data)
        pprint(self.negative_averages)
        pprint(self.positive_averages)
        pprint(self.top_highs)

    def read_json(self, path_to_json):
        with open(path_to_json) as f:
            return json.loads(f.read())[0]["results"]["predictions"]

    def get_top_n_emotions(
        self, parsed_data: dict, emotion_type: dict, top_n=3
    ) -> dict:
        """
        Averages all file segment averages to get an overall top 3 average emotions

        Parameters
        ----------
        parsed_data : dict
            data from function: parse_avg_and_high_emotions()
        top_n : int
            represents top n emotions

        Returns
        -------
        list = 
            [
                ('Calmness', {'average': 0.37940427596132786, 'str_repr': 'none to slight Calmness'}),
                ('Amusement', {'average': 0.3716967106019595, 'str_repr': 'none to slight Amusement'}),
                ('Joy', {'average': 0.3490989075306995, 'str_repr': 'none to slight Joy'})
            }
        """
        res = {}
        count = {}
        for k_file_segment, v_dict in parsed_data.items():
            for k_emotion_name, v_emotion_vals in v_dict.items():
                if emotion_type.get(k_emotion_name, None):
                    if res.get(k_emotion_name, None):
                        res[k_emotion_name]['average'] += v_emotion_vals['average']
                    else:
                        res[k_emotion_name] = {**v_emotion_vals}
                    count[k_emotion_name] = count.get(k_emotion_name, 0) + 1
                    
        for k_emotion_name, v_emotion_vals in res.items():
            res[k_emotion_name]['average'] = v_emotion_vals['average']/count[k_emotion_name]

        sorted_items = sorted(res.items(), key=lambda item: item[1]["average"], reverse=True)
        
        return sorted_items[:top_n]
    
    def get_top_n_high_emotions(self, parsed_data) -> dict:
        """
        Parse top 3 by high score emotions from data
        :param parsed_data: highs data from parse_avg_and_high_emotions()
        :return: list of top 3 highest emotions in data with timestamps
        -----
        list = 
            [
                
            ]
        """
        sorted_data = sorted(parsed_data.items(), key=lambda x: x[1]['high'], reverse=True)
        return sorted_data[:3]

    def parse_avg_and_high_emotions(self) -> dict:
        """Emotion type takes in either POSITIVE_EMOTIONS or NEGATIVE_EMOTIONS"""

        def emotion_level(emotion_average: float) -> str:
            if 0 <= emotion_average < 0.4:
                return "Low "
            elif 0.4 <= emotion_average < 0.8:
                return "Medium "
            else:
                return "High "

        file_data = {}
        highs = {} # hold highs for each emotion

        for idx, file in enumerate(self.raw_data):
            file_name = self.raw_data[idx]["file"]
            # print(f"{file_name=}")

            grouped_predictions: list[dict] = self.raw_data[idx]["models"]["face"][
                "grouped_predictions"
            ][
                0
            ]  # each dict represents frames
            grouped_predictions = grouped_predictions["predictions"]

            segment_emotion_data = {} # Average dict
            for idx, frame in enumerate(grouped_predictions):
                timestamp = frame['time'] # For highs dictionary
                num_frames = len(grouped_predictions)
                emotions: list[dict] = frame["emotions"]

                for idx, emotion in enumerate(emotions):
                    emotion_name = emotion["name"]
                    emotion_score = emotion["score"]

                    # Add scores to average dict
                    if not segment_emotion_data.get(emotion_name, None):
                        segment_emotion_data[emotion_name] = emotion_score
                    else:
                        segment_emotion_data[emotion_name] += emotion_score

                    # Update highs dict
                    if not highs.get(emotion_name, None):
                        highs[emotion_name] = {'high': 0, 'timestamp': timestamp, 'str_repr': ''}
                    else:
                        if emotion_score > highs[emotion_name]['high']:
                            highs[emotion_name]['high'] = emotion_score
                            highs[emotion_name]['str_repr'] = f"{emotion_level(emotion_score)}{emotion_name}"
                            highs[emotion_name]['timestamp'] = timestamp

            # Calculate averages from average dict
            for k_emotion, v_score in segment_emotion_data.items():
                if v_score == "":
                    continue
                average = v_score / num_frames
                segment_emotion_data[k_emotion] = {
                    "average": average,
                    "str_repr": f"{emotion_level(average)}{k_emotion}",
                }
            file_data[file_name] = segment_emotion_data
        return file_data, highs


# if __name__ == "__main__":
#     # obj = Hume_Data("outputs/sample-audio-and-face.json")
#     obj = Hume_Data("outputs/predictions.json")
#     obj.parse()
