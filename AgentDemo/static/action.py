from .. import BaseAction, AudioAction, EmojiAction, TextAction


class InsertAction(BaseAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)
        self.insert_action_prefix = action_config.get("insert_action_prefix")
        self.stage = action_config.get("stage")


class IAEAction(InsertAction, AudioAction, EmojiAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)


class IEAction(InsertAction, EmojiAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)


class TIEAction(EmojiAction, InsertAction, TextAction):
    def __init__(self, action_name: str, action_config: dict):
        super().__init__(action_name, action_config)
