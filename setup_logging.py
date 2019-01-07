import logging
import sys


def init_logging():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create STDERR handler
    handler = logging.StreamHandler(sys.stderr)
    # ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Set STDERR handler as the only handler
    logger.handlers = [handler]