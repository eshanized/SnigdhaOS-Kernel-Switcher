import subprocess
import shlex
import logging
import asyncio
import os

# Ensure logs folder exists
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "command_runner.log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class CommandRunner:
    """
    A utility class to run shell commands securely and efficiently.
    Supports synchronous and asynchronous execution.
    """

    @staticmethod
    def run_command(command, timeout=30, capture_output=True):
        """
        Runs a shell command synchronously.

        Args:
            command (str): The command to execute.
            timeout (int): The maximum time (in seconds) before timeout.
            capture_output (bool): If True, captures output; otherwise, runs without capture.

        Returns:
            dict: Contains 'stdout', 'stderr', and 'return_code'.
        """
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                shlex.split(command),
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                timeout=timeout,
                check=False,
            )

            response = {
                "stdout": result.stdout.strip() if result.stdout else "",
                "stderr": result.stderr.strip() if result.stderr else "",
                "return_code": result.returncode,
            }

            logger.info(f"Command executed successfully: {response}")
            return response

        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return {"stdout": "", "stderr": "Command timeout", "return_code": -1}

        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"stdout": "", "stderr": str(e), "return_code": -1}

    @staticmethod
    async def run_command_async(command, timeout=30, capture_output=True):
        """
        Runs a shell command asynchronously.

        Args:
            command (str): The command to execute.
            timeout (int): The maximum time (in seconds) before timeout.
            capture_output (bool): If True, captures output; otherwise, runs without capture.

        Returns:
            dict: Contains 'stdout', 'stderr', and 'return_code'.
        """
        try:
            logger.info(f"Executing async command: {command}")

            process = await asyncio.create_subprocess_exec(
                *shlex.split(command),
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                logger.error(f"Async command timeout: {command}")
                return {"stdout": "", "stderr": "Command timeout", "return_code": -1}

            response = {
                "stdout": stdout.decode().strip() if stdout else "",
                "stderr": stderr.decode().strip() if stderr else "",
                "return_code": process.returncode,
            }

            logger.info(f"Async command executed successfully: {response}")
            return response

        except Exception as e:
            logger.error(f"Async command execution failed: {e}")
            return {"stdout": "", "stderr": str(e), "return_code": -1}


# Example Usage (Uncomment to test)
if __name__ == "__main__":
    # Synchronous command execution
    print(CommandRunner.run_command("uname -r"))

    # Asynchronous command execution
    async def test_async():
        result = await CommandRunner.run_command_async("ls -la")
        print(result)

    asyncio.run(test_async())
