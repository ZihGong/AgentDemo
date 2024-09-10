import json
from logging import Logger
from typing import Callable

from pygame import Surface

from AgentDemo.base import Background, RootClass


class AreaPriority(RootClass):
    area_priority_map: dict[str, int] = {}

    def __init__(self, area_name: str, inner_priority: int):
        if area_name not in self.area_priority_map:
            raise ValueError(f"Unsupported value: {area_name}")
        self.area_name = area_name
        self.inner_priority = inner_priority
    
    def __lt__(self, other):
        if not isinstance(other, AreaPriority):
            return NotImplemented
        if self.area_priority_map[self.area_name] != self.area_priority_map[other.area_name]:
            return self.area_priority_map[self.area_name] < self.area_priority_map[other.area_name]
        return self.inner_priority < other.inner_priority
    
    def __eq__(self, other):
        if not isinstance(other, AreaPriority):
            return NotImplemented
        return (self.area_priority_map[self.area_name] == self.area_priority_map[other.area_name] and
                self.inner_priority == other.inner_priority)


class ItemObject(RootClass):
    type_map: dict[str, Callable] = {}
    
    def __init__(self, config_json: str, screen: Surface, logger: Logger = None):
        self.logger = logger
        with open(config_json, "r", encoding='utf-8') as f:
            info = json.load(f)
        info["screen"] = screen
        info["logger"] = logger
        self.priority = AreaPriority(info["area"], info["inner_priority"])
        self.object = self.type_map.get(info["type"], Background)(**info)
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority
    
    def show(self):
        self.object.show()
