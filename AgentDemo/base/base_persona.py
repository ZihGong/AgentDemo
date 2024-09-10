from logging import Logger
from typing import Generator, Callable, Optional

import pygame

from .settings import CHI, ENG
from .base_action import BaseAction, EmojiAction, AudioAction, TextAction
from .base_object import BaseObject, RootClass, ImageConfig, Position
from ..tools import add_para, is_chinese

FRAME_W = 64  # 根据你的精灵表的实际帧宽度调整
FRAME_H = 64  # 根据你的精灵表的实际帧高度调整

action_pre_process_funcs = []
frame_draw_funcs = []


def action_process(class_key):
    """
    used to register action process functions
    Args:
        class_key: the class name of self
    """
    
    def decorator(func):
        action_pre_process_funcs.append((class_key, func))
        return func
    
    return decorator


def frame_draw(class_key):
    """
    used to register frame draw functions
    Args:
        class_key: the class name of self
    """
    
    def decorator(func):
        frame_draw_funcs.append((class_key, func))
        return func
    
    return decorator


def action_regular(
        action_class: Callable,
        actions: dict,
        default_fg: Optional[list[ImageConfig]],
        default_bg: Optional[list[ImageConfig]]
):
    """
    used to instance the action class
    Args:
        default_bg:
        default_fg:
        action_class: the action class
        actions: dict to instance the action class
    Returns:
        action list
    """
    
    return [action_class(k, add_para(v, default_bg, default_fg)) for k, v in actions.items()]


class PersonaBase(RootClass):
    """
    The Base class of persona, implemented with function:
        1. process with the move and face
        2. the arg to be specified
            (x, y): location
            sprit_sheet: the image path store the sprit sheet
            action: a list of action
            screen: the surface to be draw on
    """
    
    def __init__(
            self,
            *args,
            x: float,
            y: float,
            sprit_sheet: str,
            screen: pygame.Surface,
            action: dict,
            action_class: Callable = BaseAction,
            orientation: str = "down",
            logger: Optional[Logger] = None,
            background: Optional[list[ImageConfig]] = None,
            foreground: Optional[list[ImageConfig]] = None,
            **kwargs
    ):
        
        self.position = Position(x, y)
        self.sprit_sheet = pygame.image.load(sprit_sheet).convert_alpha()
        self.screen = screen
        self.action_class = action_class
        self.action: list[BaseAction] = action_regular(self.action_class, action, foreground,
                                                       background)
        self.orientation = orientation
        self.logger = logger
        self.background = background
        self.foreground = foreground
        
        self.call_functions(action_pre_process_funcs)
        
        self.frames = self.frame_generator()
    
    def call_functions(self, funcs: list, *args, **kwargs):
        """
        used ro call the registered functions
        Args:
            funcs: the list contains the tuple (class name, function)
        """
        mro_name = [class_type.__name__ for class_type in self.__class__.__mro__][::-1]
        for class_name in mro_name:
            for key, func in funcs:
                if key == class_name:
                    func(self, *args, **kwargs)
    
    @frame_draw("PersonaBase")
    def persona_background_draw(self, object_list: list[BaseObject], action_config: BaseAction, **kwargs):
        _ = kwargs
        for p, image in action_config.background:
            object_list.append(BaseObject(self.position + p, image, self.screen))
    
    @frame_draw("PersonaBase")
    def persona_draw(self, object_list: list[BaseObject], frame_num: int, action_config: BaseAction):
        sheet_row, col_num, pace, orientation = action_config.para
        
        self.orientation = orientation
        sheet_col = (frame_num % col_num)
        self.position += pace
        
        persona_surface = self.sprit_sheet.subsurface(
            pygame.Rect(sheet_col * FRAME_W, sheet_row * FRAME_W, FRAME_W, FRAME_H))
        persona_frame = BaseObject(self.position, image=persona_surface, screen=self.screen)
        object_list.append(persona_frame)
    
    @frame_draw("PersonaBase")
    def persona_foreground_draw(self, object_list: list[BaseObject], action_config: BaseAction, **kwargs):
        _ = kwargs
        for p, image in action_config.foreground:
            object_list.append(BaseObject(self.position + p, image, self.screen))
    
    def frame_generator(self) -> Generator:
        while True:
            if len(self.action) == 0:
                self.add_default_action()
            action_config = self.action.pop(0)
            for i in range(action_config.frames):
                object_list: list[BaseObject] = []
                self.call_functions(funcs=frame_draw_funcs,
                                    object_list=object_list,
                                    frame_num=i,
                                    action_config=action_config)
                yield object_list
    
    def add_default_action(self):
        default_action_name = f"face_{self.orientation}"
        default_action_config = {"second": 1}
        default_action_config = add_para(default_action_config, self.background, self.foreground)
        self.add_action(default_action_name, default_action_config)
    
    def show(self):
        object_list: list[BaseObject] = next(self.frames)
        for o in object_list:
            o.show()
    
    def add_action(self, action_name: str, action_config: dict):
        self.action.append(self.action_class(action_name, action_config))
    
    @classmethod
    def set_cls_attr(cls, attr: str, value):
        if hasattr(cls, attr):
            setattr(cls, attr, value)
        else:
            raise ValueError(f"Attribute {attr} does not exist in class {cls.__name__}.")


class AudioPersona(PersonaBase):
    def __init__(self, **kwargs):
        kwargs.setdefault("action_class", AudioAction)
        super().__init__(**kwargs)
    
    @frame_draw("AudioPersona")
    def audio_play(self, object_list: list[BaseObject], frame_num: int, action_config: AudioAction):
        if action_config.audio is not None and frame_num == 0:
            object_list.append(BaseObject(screen=self.screen, music_audio=action_config.audio))


class EmojiPersona(PersonaBase):
    def __init__(self, **kwargs):
        kwargs.setdefault("action_class", EmojiAction)
        super().__init__(**kwargs)
    
    @action_process("EmojiPersona")
    def add_emoji_bubble(self):
        for a in self.action:
            a: EmojiAction
            if a.emoji is not None and a.speech_bubble is not None:
                a.add_persona_foreground(self.bubble_position(a), a.speech_bubble)
                a.add_persona_foreground(self.bubble_position(a), a.emoji)
    
    @staticmethod
    def bubble_position(action_config: EmojiAction):
        if "right" in action_config.speech_bubble:
            return 1, -1
        elif "left" in action_config.speech_bubble:
            return -1, -1


class TextPersona(PersonaBase):
    def __init__(self, **kwargs):
        kwargs.setdefault("action_class", TextAction)
        self.text_coordinate = Position(kwargs.get("text_x", 5), kwargs.get("text_y", 1))
        super().__init__(**kwargs)
    
    @staticmethod
    def font_config(text: str) -> tuple[str, int, tuple]:
        if is_chinese(text):
            return CHI.type, CHI.size, CHI.color
        else:
            return ENG.type, ENG.size, ENG.color
    
    @staticmethod
    def text_line_spacing(text: str):
        line_spacing = CHI.line_spacing if is_chinese(text) else ENG.line_spacing
        return 0, line_spacing
    
    @frame_draw("TextPersona")
    def text_draw(self, object_list: list[BaseObject], action_config: TextAction, **kwargs):
        _ = kwargs
        p = self.text_coordinate
        if action_config.text is not None:
            for t in action_config.text:
                font_type, font_size, font_color = self.font_config(t)
                p += self.text_line_spacing(t)
                font = pygame.font.SysFont(font_type, font_size)
                text_surface = font.render(t, True, font_color)
                object_list.append(BaseObject(p, text_surface, self.screen))
