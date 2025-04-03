import os
import logging
from logging.handlers import RotatingFileHandler

# Define Log Directory & File
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "application.log")

# Ensure logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure Logger
class Logger:
    """
    Centralized Logger for Snigdha-OS-Kernel-Switcher.
    Supports console & file logging with rotation.
    """

    def __init__(self, name="SnigdhaLogger", log_file=LOG_FILE, level=logging.DEBUG):
        """
        Initializes the logger.
        Args:
            name (str): Logger name.
            log_file (str): Path to log file.
            level (int): Logging level (default: DEBUG).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_file = log_file

        # Prevent duplicate handlers
        if not self.logger.hasHandlers():
            self._add_console_handler()
            self._add_file_handler()

    def _add_console_handler(self):
        """Adds a console handler for logging to stdout."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self):
        """Adds a file handler with log rotation."""
        file_handler = RotatingFileHandler(self.log_file, maxBytes=5 * 1024 * 1024, backupCount=3)  # 5MB file size
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """Logs a DEBUG message."""
        self.logger.debug(message)

    def info(self, message):
        """Logs an INFO message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a WARNING message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an ERROR message."""
        self.logger.error(message)

    def critical(self, message):
        """Logs a CRITICAL message."""
        self.logger.critical(message)


# Singleton Logger Instance
logger = Logger().logger

# Example Usage (Uncomment to Test)
if __name__ == "__main__":
    logger.debug("Debugging information")
    logger.info("Application started successfully")
    logger.warning("Low disk space warning")
    logger.error("Failed to load configuration file")
    logger.critical("System crash imminent!")
