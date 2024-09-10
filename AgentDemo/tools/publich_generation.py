import json
import random
from typing import Generator, Any


def random_info_generator(elements: list[Any]) -> Generator[Any, None, None]:
    random.shuffle(elements)
    
    while elements:
        yield elements.pop()


def write_json(doc_path: str,
               original_data: dict,
               image: Generator[str, None, None],
               name: Generator[str, None, None],
               stay_time: Generator[int, None, None]):
    for area, info in original_data.items():
        move_seconds = (i for i in range(info["number"], 0, -1) for _ in range(2))
        priority_list = list(range(1, info["number"] + 1))
        for i in range(info["number"]):
            a = {
                'profession': "Public",
                'name': next(name),
                'area': "Public Gallery " + area,
                'inner_priority': priority_list.pop(0),
                'type': "Persona",
                "sprit_sheet": next(image),
                'x': info['x'],
                'y': info['y'],
                "action": {"face_down": {"second": next(stay_time)}}
                
            }
            if "action" in info:
                for action, time in info["action"].items():
                    if "random" in time:
                        time = {"second": next(move_seconds)}
                    a["action"][action] = time
            
            if "out_action" in info:
                a["out_action"] = {}
                for action, time in info["out_action"].items():
                    if "random" in time:
                        time = {"second": next(move_seconds)}
                    a["out_action"][action] = time
            file_path = doc_path + "Public_" + area + "_" + str(i) + ".json"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(a, file, ensure_ascii=False, indent=4)


# TODO: set a same time that all guys stop in action
#       wait, up, random, down, face_up

def public_generation(src_path, dst_path):
    with open(src_path, 'r') as file:
        data = json.load(file)
    
    stay_time = random_info_generator(list(range(0, data['stay_time'], 2)))
    image = random_info_generator(list(data['sprit_sheet'].values()))
    name = random_info_generator(list(data['names'].values()))
    
    write_json(dst_path, data["info"], image, name, stay_time)

## 生成的更加靠后的不可以踩人，也就是位置在后面的，座位要在中间
# image：rand
# stay：rand
# pace：先生成两边的
# 简直天才
