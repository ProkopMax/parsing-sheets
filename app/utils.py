import time
import logging

def get_time():
    try:
        curr_time = time.strftime("%H:%M", time.localtime())
        return curr_time
    except:
        print("Ошибка получения ВРЕМЕНИ")

def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


