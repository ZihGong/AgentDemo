# classroom/settings.py
from dataclasses import dataclass


@dataclass
class ImageConfig:
    x: int
    y: int
    path: str


class Color:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


@dataclass
class FontConfig:
    type: str = "songti"
    size: int = 17
    color: tuple = Color.BLACK
    line_spacing: float = 0.8
    line_length: int = 60


CHI = FontConfig()
ENG = FontConfig(type="songti", size=20, line_spacing=0.8, line_length=50)

if __name__ == '__main__':
    print(MAIN.size)
    print(CHI.color)
    i = ImageConfig(1, 2, "yew")
    print(i)
