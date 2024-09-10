import io
from dataclasses import dataclass
from typing import Optional, Union

import pygame
from objprint import add_objprint
from pygame import Surface
from pygame.mixer import music, Sound

from .settings import GameConfig


@dataclass
class ImageConfig:
    x: int
    y: int
    path: str


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        elif isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Operand must be a tuple of length 2 or another Position")
    
    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"
    
    def __len__(self):
        return 2


@add_objprint
class RootClass(object):
    @classmethod
    def set_cls_attr(cls, attr: str, value):
        if hasattr(cls, attr):
            setattr(cls, attr, value)
        else:
            raise ValueError(f"Attribute {attr} does not exist in class {cls.__name__}.")


@add_objprint
class BaseObject(RootClass):
    def __init__(
            self,
            position: Optional[Position] = None,
            image: Optional[Union[str, Surface]] = None,
            screen: Optional[Surface] = None,
            music_audio: Optional[Union[str, io.BytesIO]] = None,
            sound_audio: Optional[Union[str, io.BytesIO]] = None,
    ):
        """
        The Base class contains image, backgound music and sound effect
        Args:
            image: image path or surface
            screen: screen to be draw on
            music_audio: audio path
            sound_audio: audio path or bytes object
        """
        
        self.position = position
        self.screen = screen
        self.music_audio = music_audio
        self.sound_audio = sound_audio
        
        self.image = self.image_process(image)
    
    @staticmethod
    def image_process(image):
        if isinstance(image, str):
            return pygame.image.load(image).convert_alpha()
        elif isinstance(image, Surface):
            return image
        return None
    
    def show(self, position: Optional[Position] = None):
        draw_p = position if position is not None else self.position
        
        if self.image is not None:
            self.screen.blit(self.image, (draw_p.x * GameConfig.tile_size, draw_p.y * GameConfig.tile_size))
        
        if self.music_audio is not None:
            music.load(self.music_audio)
            music.play()
        
        if self.sound_audio is not None:
            Sound(self.sound_audio).play()


class Background(BaseObject):
    def __init__(
            self,
            init_x: float,
            init_y: float,
            image: Union[str, Surface],
            screen: Surface,
            **kwargs
    ):
        super().__init__(Position(init_x, init_y), image, screen)
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.x_interval: Optional[int] = None
        self.y_interval: Optional[int] = None
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def show(self, x=None, y=None):
        if self.width is None:
            super().show()
        else:
            for i in range(0, self.width * self.x_interval, self.x_interval):
                for j in range(0, self.height * self.y_interval, self.y_interval):
                    super().show(self.position + (i, j))
