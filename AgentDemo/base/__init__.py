from .base_action import BaseAction, EmojiAction, AudioAction, TextAction
from .base_object import BaseObject, Background, RootClass
from .base_persona import PersonaBase, EmojiPersona, AudioPersona, TextPersona, action_process, frame_draw
from .item import AreaPriority, ItemObject
from .scene import Scene
from .settings import CHI, ENG, print_config, GameConfig, SceneConfig

# 设置包的公开接口
__all__ = ['GameConfig', "print_config", "CHI", "ENG",
           "EmojiAction", "AudioAction", "TextAction", "BaseAction",
           "EmojiPersona", "AudioPersona", "TextPersona", "PersonaBase", "action_process", "frame_draw",
           "BaseObject", "Background", "RootClass",
           "AreaPriority", "ItemObject",
           "Scene", "SceneConfig"]
