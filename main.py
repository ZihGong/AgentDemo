import logging

from AgentDemo import (AreaPriority, Background, EIPersona, EITPersona,
                       FreeLogger, GameConfig, InsertPersona, ItemObject,
                       load_json, EmojiAction)
from examples.classroom.game import Game

logger = FreeLogger(
    'my_logger',
    include=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
)


def main_classroom():
    GameConfig.title = "Classroom"
    config = load_json("examples/classroom/assets/config.json")
    InsertPersona.set_cls_attr("insert_file_map", config["insert_file_map"])
    AreaPriority.set_cls_attr("area_priority_map", config["area_priority_map"])
    
    type_map = {
        "Persona": EIPersona,
        "TextPersona": EITPersona,
        "Background": Background
    }
    ItemObject.set_cls_attr("type_map", type_map)
    
    EmojiAction.set_cls_attr("emoji_path_map", config["emoji_path_map"])
    EmojiAction.set_cls_attr("speechbubble_path_map", config["speechbubble_path_map"])
    
    # GAME STRAT
    game = Game(logger)
    game.run()


if __name__ == '__main__':
    main_classroom()
