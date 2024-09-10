import os
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


@dataclass
class TextImageConfig:
    text_position: tuple[int, int] = (2, 2)
    text_color: tuple[int, int, int, int] = (0, 0, 0, 255)
    
    font_size: int = 24
    font_path: str = "/System/Library/Fonts/PingFang.ttc"
    image_size: tuple[int, int] = (64, 32)
    image_color: tuple[int, int, int, int] = (255, 255, 255, 0)


def get_text_image(config: TextImageConfig, save_path, text: str):
    image = Image.new('RGBA', config.image_size, config.image_color)
    font = ImageFont.truetype(config.font_path, config.font_size)
    draw = ImageDraw.Draw(image)
    draw.text(config.text_position, text, font=font, fill=config.text_color)
    image.save(save_path)


def get_text_images(save_folder: str, texts: list[str]):
    for text in texts:
        save_path = os.path.join(save_folder, f"{text}.png")
        get_text_image(TextImageConfig(), save_path, text)


if __name__ == '__main__':
    get_text_images(texts=["教师", "考官", "学生", "分析"], save_folder="../assets/image/font")
