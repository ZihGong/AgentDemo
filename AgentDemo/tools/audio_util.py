import math
import os
import re
from typing import List

from mutagen.mp3 import MP3
from pydub import AudioSegment


def natural_sort_key(s: str):
    # 提取数字并将其转换为整数，其余部分保持原样
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def sort_files_naturally(file_list: List[str]) -> List[str]:
    return sorted(file_list, key=natural_sort_key)


def merge_mp3(ori_path, output_path, silence_duration=500):
    # 获取文件夹中所有 MP3 文件的路径
    file_paths = [os.path.join(ori_path, f) for f in os.listdir(ori_path)]
    folder_paths = [f for f in file_paths if os.path.isdir(f)]
    for folder_path in folder_paths:
        folder_name = os.path.basename(folder_path)
        mp3_files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
        # 按文件名排序
        mp3_files = sort_files_naturally(mp3_files)
        print(mp3_files)
        # 创建一个空音频对象
        combined = AudioSegment.empty()
        # 创建间隔的空白音频
        # silence = AudioSegment.silent(duration=silence_duration)
        
        for mp3_file in mp3_files:
            print(mp3_file)
            mp3_path = os.path.join(folder_path, mp3_file)
            audio = AudioSegment.from_mp3(mp3_path)
            # 将音频文件和间隔音频添加到组合音频中
            combined += audio
        
        # 导出合并后的音频到指定路径
        p = os.path.join(output_path, folder_name) + ".mp3"
        combined.export(p, format='mp3')
        
        print(f"合并后的音频已保存到 {p}")


def mp3_time(mp3_path):
    audio = MP3(mp3_path)
    total_duration = audio.info.length
    
    return math.ceil(total_duration * 4)


if __name__ == '__main__':
    output_path = "../assets/audio/au2"
    
    merge_mp3("../assets/audio/tmp", output_path)
