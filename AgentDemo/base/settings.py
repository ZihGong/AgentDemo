from dataclasses import dataclass


@dataclass
class GameConfig:
    tile_size: int = 32
    game_fps: int = 32
    base_fps: int = 8
    title: str = "Agent"
    pace: int = 4  # pace = tile_size/ base_fps, Constant


@dataclass
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


@dataclass
class SceneConfig:
    coordinate: tuple[int, int] = (0, 0)
    size: tuple[int, int] = (0, 0)
    
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if isinstance(value, (int, float)):
            return value * GameConfig.tile_size
        elif isinstance(value, tuple):
            return tuple(v * GameConfig.tile_size for v in value)
        return value


def print_config():
    print(GameConfig.title)
