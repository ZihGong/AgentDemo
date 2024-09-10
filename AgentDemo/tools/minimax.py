import json
import os
import time

import requests

from config import *

from tqdm import tqdm

SOURCE = {
    # "clerk": "../assets/school/persona/stu.json",
    # "chief_judge": "../assets/school/persona/examiner.json",
    # "plaintiff_lawyer": "../assets/school/persona/teacher.json",
    "defence_lawyer": "../assets/school/persona/assaying.json"
}

VOICE = {
    "clerk": "presenter_female",
    "chief_judge": "male-qn-jingying-jingpin",
    "plaintiff_lawyer": "male-qn-jingying",
    "defence_lawyer": "female-chengshu-jingpin"
}

DESTINATION = "../assets/audio"


def my_sleep(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        time.sleep(4)
        return result
    
    return wrapper


@my_sleep
def request_audio(text: str, voice: str) -> str:
    data["text"] = text
    data["voice_id"] = voice
    response = requests.post(URL, headers=HEADERS, json=data)
    if response.status_code != 200:
        raise ValueError(f"Request failed with {response.status_code = } and {response.json() = }")
    return response.json()["audio_file"]


def save_audio(content: bytes, folder_path: str, index: int):
    file_path = os.path.join(folder_path, f"{index}.mp3")
    with open(file_path, 'wb') as file:
        file.write(content)


@my_sleep
def download_audio(url: str) -> bytes:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Request failed with {response.status_code = } and {response.json() = }")
        return response.content
    except ValueError:
        raise ValueError(f"Request failed with {url}")


def handle(action_name: str, action_info: dict):
    description = action_info.get("description")
    if description is not None:
        return action_name, description


def main():
    for persona_name, json_file in SOURCE.items():
        voice = VOICE[persona_name]
        persona_folder = os.path.join(DESTINATION, persona_name)
        with open(json_file, "r") as f:
            persona_config = json.load(f)
        action = persona_config["action"]
        
        description_list = map(handle, action.keys(), action.values())
        description_list = list(filter(lambda x: x is not None, description_list))
        
        for action_name, description in tqdm(description_list, desc=persona_name):
            action_folder = os.path.join(persona_folder, action_name)
            os.makedirs(action_folder, exist_ok=True)
            for i, text in enumerate(description):
                url = request_audio(text, voice)
                mp3 = download_audio(url)
                save_audio(mp3, action_folder, i)


if __name__ == "__main__":
    main()
