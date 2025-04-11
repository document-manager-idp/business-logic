import os
import sys
import logging
from config import Config

def get_logger(
    name,
    log_dir=None,
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s: %(message)s",
    stderr=False
) -> logging.Logger:
    log_dir = log_dir or Config.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        fileHandler = logging.FileHandler(f'{log_dir}/{name}.log')
        fileHandler.setFormatter(logging.Formatter(format))
        logger.addHandler(fileHandler)

        if stderr:
            streamHandler = logging.StreamHandler(sys.stderr)
            streamHandler.setFormatter(logging.Formatter(format))
            logger.addHandler(streamHandler)

    return logger
