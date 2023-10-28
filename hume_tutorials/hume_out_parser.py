import json
from pprint import pprint


class Hume_Data:
    def __init__(self, path_to_json):
        # self.raw_data = json.load(path_to_json)["results"]["predictions"] # Get every file analysis
        self.raw_data = self.read_json(path_to_json)

    def wrapper(self):
        file_data = {}

        for idx, raw_dict in enumerate(self.raw_data):
            # print(f"{idx=}")
            # print(f"{raw_dict=}")
            file_data[self.raw_data[idx]["file"]] = {}
        pprint(file_data)


    def read_json(self, path_to_json):
        with open(path_to_json) as f:
            return json.loads(f.read())[0]["results"]["predictions"]

    # def get_emotions()


if __name__ == "__main__":
    obj = Hume_Data("Sample-Outputs/sample-audio-and-face.json")
    obj.wrapper()
