from .text_util import split_by_length, is_chinese
from .utils import add_para, load_json
from .free_logger import FreeLogger

# 设置包的公开接口
__all__ = ['split_by_length', "add_para", "is_chinese", "load_json", "FreeLogger"]
