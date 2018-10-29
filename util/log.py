# -*- coding:utf-8 -*-
from baidumap.core import static

DEBUG = static.DEBUG
INFO = static.INFO
WARNING = static.WARNING
ERROR = static.ERROR
NONE = static.NONE


mode = WARNING
logger = NONE


def load_config():
    global mode, logger
    baidu = __import__('baidumap.config')
    mode = baidu.config.mode
    logger = baidu.config.logger


def is_valid(rank):
    global mode
    load_config()
    if not isinstance(mode, int):
        mode = 2
    return rank >= mode


def debug(msg):
    if is_valid(DEBUG):
        if logger is None:
            print('[DEBUG]%s' % msg)
        else:
            logger.debug(msg)
    return


def info(msg):
    if is_valid(INFO):
        if logger is None:
            print('[INFO]%s' % msg)
        else:
            logger.info(msg)
    return


def warning(msg):
    if is_valid(WARNING):
        if logger is None:
            print('[WARNING]%s' % msg)
        else:
            logger.warning(msg)
    return


def error(msg):
    if is_valid(NONE):
        if logger is None:
            print('[ERROR]%s' % msg)
        else:
            logger.error(msg)
    return
