import json
import re

import chardet

source_file = ""
destination_file = ""

# 示例字符串
text = "这是第一行\n这是第二行\n\n这是第三行"

# 根据 \n 或 \n\n 分割字符串
parts = re.split(r'\n{1,2}', text)

print(isinstance(parts, list))


def main1():
    with open(source_file, 'r', encoding='utf-8') as f:
        talks = json.load(f)
    
    answer = []
    for talk in talks:
        talk["content"] = re.split(r'\n{1,2}', talk["content"])
        print(talk)
    
    with open(destination_file, 'w', encoding='utf-8') as f:
        json.dump(talks, f, ensure_ascii=False, indent=4)


def main2():
    with open("../assets/static/school/persona/examiner.json", 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        print(result)


if __name__ == "__main__":
    main2()
