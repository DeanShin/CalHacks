import os
from pathlib import Path
import pprint

from .hume_out_parser import Hume_Data, POSITIVE_EMOTIONS, NEGATIVE_EMOTIONS


from pprint import pprint

# current_directory = os.path.dirname(os.path.abspath(__file__))
# DEAN_VIDEO = "Dean-Input.mp4"
# DEAN_VIDEO = os.path.join(current_directory, DEAN_VIDEO)
# DEAN_DATA_DIR = os.path.join(current_directory, "Dean-Data")

# HUME_DIR = os.path.join(current_directory, "..")
# # RAW_DEAN_DATA = 


async def get_dean_set_content():
    ...

def get_dean_top_emotions():
    ...
    path = f'{Path(__file__).parents[0]}/outputs/predictions.json'
    hume_parser = Hume_Data(path_to_json=path)
    hume_parser.parse()
    pprint(hume_parser.top_highs)
    res = []
    for emotion, dict_granular_details in hume_parser.top_highs: # iterating through tuples
        res.append(dict_granular_details["str_repr"])
    return res

async def get_dean_key_moments():
    ...

if __name__ == "__main__":
    top_emotions = get_dean_top_emotions()
    # pprint(top_emotions)
