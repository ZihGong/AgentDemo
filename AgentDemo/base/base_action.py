from typing import Optional

from objprint import add_objprint

from ..tools import split_by_length
from .settings import CHI, ENG, GameConfig
from .base_object import ImageConfig, Position, RootClass

PACE = GameConfig.pace
UP, DOWN, LEFT, RIGHT, STAY = (0, -PACE), (0, PACE), (-PACE, 0), (PACE, 0), (0, 0)

MOVE_COL, HELLO_COL, FACE_COL = 8, 6, 1
UP_ROW, LEFT_ROW, DOWN_ROW, RIGHT_ROW = 8, 9, 10, 11


@add_objprint
class BaseAction(RootClass):
    __action_para = {
        "face_down": [DOWN_ROW, FACE_COL, STAY, "down"],
        "face_up": [UP_ROW, FACE_COL, STAY, "up"],
        "face_left": [LEFT_ROW, FACE_COL, STAY, "left"],
        "face_right": [RIGHT_ROW, FACE_COL, STAY, "right"],
        "move_up": [UP_ROW, MOVE_COL, UP, "up"],
        "move_down": [DOWN_ROW, MOVE_COL, DOWN, "down"],
        "move_left": [LEFT_ROW, MOVE_COL, LEFT, "left"],
        "move_right": [RIGHT_ROW, MOVE_COL, RIGHT, "right"],
    }
    
    def __init__(self, action_name: str, config: dict):
        self.operation = next((o for o in self.__action_para.keys() if o in action_name), action_name)
        
        second = config.get("second")
        if self.legal_operation():
            self.frames = GameConfig.base_fps * second
        
        self.background = [ImageConfig(*g) for g in config.get("background")]
        self.background = [[Position(g.x, g.y), g.path] for g in self.background]
        
        self.foreground = [ImageConfig(*g) for g in config.get("foreground")]
        self.foreground = [[Position(g.x, g.y), g.path] for g in self.foreground]
        
        if not isinstance(self.background, list):
            raise TypeError(f"wrong type of persona_background {type(self.background) = }")
    
    def add_persona_background(self, relative_pos: tuple, background_image):
        self.background.append([Position(*relative_pos), background_image])
    
    def add_persona_foreground(self, relative_pos: tuple, background_image):
        self.foreground.append([Position(*relative_pos), background_image])
    
    @property
    def para(self):
        if self.operation in self.__action_para.keys():
            return self.__action_para[self.operation]
    
    def legal_operation(self):
        return self.operation in self.__action_para.keys()
    
    def orientation(self):
        return self.__action_para[self.operation][-1] if self.legal_operation() else None


class AudioAction(BaseAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)
        self.audio: Optional[str] = action_config.get("audio")
        if self.audio is not None and not isinstance(self.audio, str):
            raise TypeError(f"wrong type of audio {type(self.audio) = }")


class EmojiAction(BaseAction):
    """
    two property: emoji, speech_bubble,
    standard input: "emoji": "hammer", or "emoji": "hammer_left"
    """
    emoji_path_map = {}
    speechbubble_path_map = {}
    
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)
        emoji = action_config.get("emoji")
        if emoji is not None:
            if emoji in self.emoji_path_map:
                self.emoji = self.emoji_path_map[emoji]
                self.speech_bubble = self.speechbubble_path_map["right"]
            else:
                self.emoji = self.emoji_path_map[emoji.split("_")[0]]
                self.speech_bubble = self.speechbubble_path_map[emoji.split("_")[1]]
        else:
            self.emoji, self.speech_bubble = None, None


class TextAction(BaseAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)
        self.text = action_config.get("text")
        if isinstance(self.text, list):
            self.text = [line for s in self.text for line in split_by_length(s, CHI.line_length, ENG.line_length)]
