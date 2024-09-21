""" This module is used to create a logger for the project. The logger will write logs to the log folder.
    Example:
        from my_logger import logger
        logger.info("This is an info message")
        logger.error("This is an error message")
        logger.warning("This is a warning message")
        logger.debug("This is a debug message")
"""
# Ensure the logger is correctly configured in `MyLogger.py`
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from common import LOG_FILE
import os

class SingletonLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonLogger, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        MAX_BYTES = 2 * 1024 * 1024  # 2MB per file
        BACKUP_COUNT = 5  # 5 backup files
        MAX_FOLDER_SIZE = 200 * 1024 * 1024  # 200MB

        # create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # make sure the logger's level is set to DEBUG

        # create a folder to store logs
        if not os.path.exists(LOG_FILE):
            os.makedirs(LOG_FILE)

        # create a file handler with a specific naming convention
        log_file = os.path.join(LOG_FILE, f'Abbott_log_{datetime.now().strftime("%m%d%y_%H%M%S")}.log')
        fh = RotatingFileHandler(log_file, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding='utf-8')
        fh.setLevel(logging.DEBUG)  # set handler's level to DEBUG

        # define the formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add the handler to the logger
        self.logger.addHandler(fh)

        # Add a custom handler to check folder size after each log write
        self.logger.addHandler(self._create_folder_size_check_handler(MAX_FOLDER_SIZE))

    def _create_folder_size_check_handler(self, max_folder_size):
        class FolderSizeCheckHandler(logging.Handler):
            def emit(self, record):
                log_files = [os.path.join(LOG_FILE, f) for f in os.listdir(LOG_FILE) if os.path.isfile(os.path.join(LOG_FILE, f))]
                total_size = sum(os.path.getsize(f) for f in log_files)

                while total_size > max_folder_size and log_files:
                    oldest_file = min(log_files, key=os.path.getctime)
                    os.remove(oldest_file)
                    log_files.remove(oldest_file)
                    total_size = sum(os.path.getsize(f) for f in log_files)

        return FolderSizeCheckHandler()

# Create a singleton logger instance
logger = SingletonLogger().logger