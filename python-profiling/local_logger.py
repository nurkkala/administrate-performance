import logging


def create_module_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter(
        fmt='%(asctime)s %(filename)s:%(lineno)d (%(funcName)s) %(message)s',
        datefmt="[%Y-%m-%d %H:%M:%S]"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_module_logger():
    return logging.getLogger(__name__)
