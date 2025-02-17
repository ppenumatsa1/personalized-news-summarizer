import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Define log directory and ensure it exists
    log_directory = os.path.abspath(os.path.join(os.getcwd(), "backend/app/logs"))
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        print(f"Created log directory at {log_directory}")
    else:
        print(f"Log directory already exists at {log_directory}")

    # Create and configure the 'summarizer' logger
    logger = logging.getLogger("summarizer")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent logs from being propagated to the root logger

    # Check if handlers are already added to prevent duplication
    if not logger.handlers:
        # Rotating File Handler
        rotating_file_handler = RotatingFileHandler(
            os.path.join(log_directory, "summarizer.log"),
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,  # Keep up to 5 backup files
        )
        rotating_file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
        )
        rotating_file_handler.setFormatter(file_formatter)

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)

        # Add handlers to the logger
        logger.addHandler(rotating_file_handler)
        logger.addHandler(stream_handler)
        print("Logging handlers added to 'summarizer' logger.")

    return logger


# Initialize logger
logger = setup_logging()


def log_exception(e):
    logger.error("An exception occurred", exc_info=e)


def log_info(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


# Add a test log to verify the logging setup
logger.info("Test log to verify logging setup")
