import logging
import sys

# Create a logger instance for the application
logger = logging.getLogger("business_logic")
logger.setLevel(logging.DEBUG)  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Create a console handler that outputs logs to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Define a log format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add the handler to the logger instance
logger.addHandler(console_handler)

# Convenience functions for logging at various levels
def debug(message, *args, **kwargs):
    logger.debug(message, *args, **kwargs)

def info(message, *args, **kwargs):
    logger.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):
    logger.warning(message, *args, **kwargs)

def error(message, *args, **kwargs):
    logger.error(message, *args, **kwargs)
