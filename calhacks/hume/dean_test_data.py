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


def get_dean_set_content() -> str:
    return """
    Clarity and Confidence: When answering questions about technical topics, it's essential to provide clear and confident responses. Avoid hesitations like "umm" and "uh" to appear more knowledgeable.

    Define the Purpose: Start by clearly stating what the chmod command does, such as "The chmod command is used to change the permissions or access mode of a file in a Unix-like operating system."

    Explain the Options: Mention that chmod offers various options to modify permissions, including read, write, and execute permissions. For example, "With chmod, you can add or remove read, write, and execute permissions on a file or directory."

    Practice: Practice your answers to common technical interview questions to ensure you can respond confidently and without hesitations.

    By following these guidelines, the interviewee can improve their answer and present themselves more effectively during a technical interview.
    """

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
