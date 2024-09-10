import logging
import os
from typing import Callable

from pygame import Surface

from .item import ItemObject


class Scene:
    def __init__(
            self,
            scene_dic: str,
            screen: Surface,
            item_class: Callable = ItemObject,
            logger: logging.Logger = None,
    ):
        """
        :param scene_dic: all the json need to be draw in this scene
        :param screen: the surface which will be drawn
        :param item_class: if you want to use your own item class, which inherits from ItemObject
        """
        self.items = []
        self.logger = logger
        for root, _, files in os.walk(scene_dic):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith("json"):
                    self.items.append(item_class(file_path, screen, logger=self.logger))
        list.sort(self.items)
    
    def draw(self):
        for item in self.items:
            item.show()
