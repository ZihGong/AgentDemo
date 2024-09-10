import logging


class LogLevelFilter(logging.Filter):
    def __init__(self, include, exclude):
        super().__init__()
        self.include = include
        self.exclude = exclude
        if self.include is None and self.exclude is None:
            raise ValueError("Either include or exclude must be set")
    
    def filter(self, record):
        if self.include is not None:
            return any(le == record.levelno for le in self.include)
        if self.exclude is not None:
            return all(le != record.levelno for le in self.exclude)


class LogFormatter(logging.Formatter):
    COLOR_DICT = {
        "BLACK": "\033[90m",
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "ORANGE": "\033[94m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
        'RESET': '\033[0m'
    }
    COLORS = {
        'DEBUG': "CYAN",
        'INFO': "GREEN",
        'WARNING': "YELLOW",
        'ERROR': 'ORANGE',
        'CRITICAL': 'RED',
        'RESET': 'RESET',
    }
    
    def __init__(self, fmt_log_level=True, datefmt=None, style='%'):
        fmt = None
        if fmt_log_level:
            fmt = "[%(levelname)-8s]: %(message)s"
        super().__init__(fmt, datefmt, style)
    
    def format(self, record):
        # 自定义逻辑（如果需要）
        # 例如添加自定义属性
        log_name = record.levelname
        log_color = self.COLOR_DICT[self.COLORS[log_name]]
        reset_color = self.COLOR_DICT[self.COLORS['RESET']]
        
        # 调用父类的 format 方法以获得默认或自定义的格式化输出
        formatted_message = super().format(record)
        
        # 在默认或自定义的格式化输出基础上进行进一步自定义
        return f"{log_color}{formatted_message}{reset_color}"


class FreeLogger(logging.Logger):
    def __init__(
            self,
            name,
            level=logging.DEBUG,
            filename=None,
            filemode=None,
            console: bool = True,
            include=None,
            exclude=None,
            fmt_log_level=False,
    ):
        """
        Args:
            name:
            level:
            filename:
            filemode:
            console: if print in console
            include: list of logging level you want to print
            exclude: list of logging level you dont want to print
        """
        super().__init__(name, level)
        
        myf = LogFormatter(fmt_log_level=fmt_log_level)
        log_filter = None
        if include is not None and exclude is not None:
            log_filter = LogLevelFilter(include=include, exclude=exclude)
        
        if filename is not None:
            file_handler = logging.FileHandler(filename, mode=filemode)
            file_handler.setLevel(level)
            file_handler.setFormatter(myf)
            if log_filter is not None:
                file_handler.addFilter(log_filter)
            self.addHandler(file_handler)
        
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(myf)
            if log_filter is not None:
                console_handler.addFilter(log_filter)
            self.addHandler(console_handler)


if __name__ == '__main__':
    # 使用自定义的 Logger
    logger = FreeLogger('my_logger', include=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL])
    logger.debug('This is a debug message')
    logger.info('This is an info message')  # This will not be logged due to the filter
    logger.warning('This is a warning message')
    logger.error('This is an error message')  # This will not be logged due to the filter
    logger.critical('This is a critical message')
