import logging
import logging.config
from os import path


def pwd(*args):
    """
    返回当前项目（或文件？）绝对路径
    :param args:
    :return:
    """
    # 不能调用theprimone中的pwd()方法，否则编译异常
    return path.join(path.dirname(__file__), *args)


# 定义三种日志输出格式
STANDARD_FORMAT = "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]"

SIMPLE_FORMAT = "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s"

ID_SIMPLE_FORMAT = "[%(levelname)s][%(asctime)s] %(message)s"

# logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
# 如果不存在定义的日志目录就创建一个
# if not os.path.isdir(logfile_dir):
#     os.mkdir(logfile_dir)

LOG4POCKET48_PATH = pwd("log", "prim.log")

LOGGING_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": STANDARD_FORMAT
        },
        "simple": {
            "format": SIMPLE_FORMAT
        },
    },
    "filters": {},
    "handlers": {
        # 打印到终端的日志
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",  # 打印到屏幕
            "formatter": "simple"
        },
        # 写入到文件的日志,收集info及以上的日志
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",  # 保存到文件
            "formatter": "standard",
            "filename": LOG4POCKET48_PATH,  # 日志文件
            "maxBytes": 1024 * 1024 * 5,  # 日志大小 5M
            "backupCount": 5,
            "encoding": "utf-8",  # 日志文件的编码
        },
    },
    "loggers": {
        "prim": {
            "handlers": ["default", "console"],
            "level": "DEBUG",
            "propagate": True,  # 向上（更高level的logger）传递
        },
    },
}


def get_logger(logger_name):
    logging.config.dictConfig(LOGGING_DICT)  # 导入配置
    return logging.getLogger(logger_name)


if __name__ == "__main__":
    logger = get_logger("prim")
    logger.info("hello world.")
