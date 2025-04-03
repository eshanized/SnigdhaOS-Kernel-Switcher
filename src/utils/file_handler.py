import os
import json
import shutil
import logging

# Ensure logs folder exists
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "file_handler.log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class FileHandler:
    """
    Utility class for handling file and directory operations.
    """

    @staticmethod
    def read_file(file_path, mode="r"):
        """
        Reads a file and returns its content.

        Args:
            file_path (str): Path to the file.
            mode (str): File reading mode (default: "r" for text).

        Returns:
            str: Content of the file or None if an error occurs.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        try:
            with open(file_path, mode, encoding="utf-8") as file:
                content = file.read()
                logger.info(f"File read successfully: {file_path}")
                return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

    @staticmethod
    def write_file(file_path, content, mode="w"):
        """
        Writes content to a file.

        Args:
            file_path (str): Path to the file.
            content (str): Content to write.
            mode (str): File writing mode (default: "w" to overwrite).

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(file_path, mode, encoding="utf-8") as file:
                file.write(content)
                logger.info(f"File written successfully: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            return False

    @staticmethod
    def read_json(file_path):
        """
        Reads a JSON file and returns its contents as a dictionary.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict: JSON content or None if an error occurs.
        """
        content = FileHandler.read_file(file_path)
        if content is None:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON file {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path, data):
        """
        Writes a dictionary as a JSON file.

        Args:
            file_path (str): Path to the JSON file.
            data (dict): Data to write.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            json_content = json.dumps(data, indent=4)
            return FileHandler.write_file(file_path, json_content)
        except TypeError as e:
            logger.error(f"Error encoding JSON data for {file_path}: {e}")
            return False

    @staticmethod
    def file_exists(file_path):
        """
        Checks if a file exists.

        Args:
            file_path (str): Path to the file.

        Returns:
            bool: True if file exists, False otherwise.
        """
        exists = os.path.exists(file_path)
        logger.info(f"File exists check ({file_path}): {exists}")
        return exists

    @staticmethod
    def delete_file(file_path):
        """
        Deletes a file if it exists.

        Args:
            file_path (str): Path to the file.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        if not os.path.exists(file_path):
            logger.warning(f"File not found for deletion: {file_path}")
            return False
        try:
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

    @staticmethod
    def create_directory(dir_path):
        """
        Creates a directory if it does not exist.

        Args:
            dir_path (str): Path to the directory.

        Returns:
            bool: True if created successfully, False otherwise.
        """
        if os.path.exists(dir_path):
            logger.info(f"Directory already exists: {dir_path}")
            return True
        try:
            os.makedirs(dir_path)
            logger.info(f"Directory created: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            return False

    @staticmethod
    def delete_directory(dir_path):
        """
        Deletes a directory and its contents.

        Args:
            dir_path (str): Path to the directory.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        if not os.path.exists(dir_path):
            logger.warning(f"Directory not found for deletion: {dir_path}")
            return False
        try:
            shutil.rmtree(dir_path)
            logger.info(f"Directory deleted: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting directory {dir_path}: {e}")
            return False


# Example Usage (Uncomment to test)
if __name__ == "__main__":
    # File Handling
    test_file = "test.txt"
    FileHandler.write_file(test_file, "Hello, Snigdha-OS!")
    print(FileHandler.read_file(test_file))

    # JSON Handling
    test_json = "test.json"
    FileHandler.write_json(test_json, {"kernel": "5.15.0", "arch": "x86_64"})
    print(FileHandler.read_json(test_json))

    # File Existence & Deletion
    print(FileHandler.file_exists(test_file))
    FileHandler.delete_file(test_file)
    print(FileHandler.file_exists(test_file))

    # Directory Management
    test_dir = "test_dir"
    FileHandler.create_directory(test_dir)
    FileHandler.delete_directory(test_dir)
