import logging


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


# Create handlers for each level
info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_handler.addFilter(LevelFilter(logging.INFO))
info_handler.setFormatter(logging.Formatter("%(asctime)s [INFO] %(message)s"))

warning_handler = logging.StreamHandler()
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(LevelFilter(logging.WARNING))
warning_handler.setFormatter(logging.Formatter("%(asctime)s [WARNING] %(message)s"))

error_handler = logging.StreamHandler()
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(LevelFilter(logging.ERROR))
error_handler.setFormatter(logging.Formatter("%(asctime)s [ERROR] %(message)s"))

# Create a logger and add the handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to lowest level
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
