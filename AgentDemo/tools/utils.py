import json


def add_para(action_config: dict, default_bg, default_fg):
    bg = default_bg if default_bg is not None else []
    fg = default_fg if default_fg is not None else []
    action_config.setdefault("background", []).extend(bg)
    action_config.setdefault("foreground", []).extend(fg)
    return action_config


def load_json(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)
