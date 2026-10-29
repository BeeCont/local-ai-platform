"""Utilities for validating and executing external commands."""

import math
import subprocess
import time
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from local_ai_platform.logging_config import get_logger

logger = get_logger("core.command_runner")


class CommandStatus(Enum):
    """Possible outcomes of an external command execution."""

    SUCCESS = "success"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    EXECUTION_ERROR = "execution_error"


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Represent the outcome of an external command execution.

    Attributes:
        command: Executable and its arguments.
        status: Final status of the execution.
        returncode: Process exit code, if available.
        stdout: Captured standard output.
        stderr: Captured standard error.
        duration_seconds: Execution duration in seconds.
        error: Description of an execution error, if any.
    """

    command: tuple[str, ...]
    status: CommandStatus
    returncode: int | None
    stdout: str
    stderr: str
    duration_seconds: float
    error: str | None = None

    @property
    def success(self) -> bool:
        """Return whether the command completed successfully."""
        return self.status is CommandStatus.SUCCESS


def validate_command(command: Sequence[str]) -> None:
    """Validate a command and its arguments.

    Args:
        command: Executable name followed by its arguments.

    Raises:
        TypeError: If the command is not a sequence of strings.
        ValueError: If the command is empty or contains invalid arguments.
    """
    # Validate that the command is a sequence of strings and not
    # a single string or bytes.
    if isinstance(command, (str, bytes)) or not isinstance(command, Sequence):
        raise TypeError("Command must be a sequence of strings.")

    if not command:
        raise ValueError("Command cannot be empty.")

    # Validate each argument in the command.
    for index, argument in enumerate(command):
        if not isinstance(argument, str):
            raise TypeError(f"Command argument at index {index} must be a string.")
        # Validate that the argument does not contain null bytes, which can cause issues
        # in command execution.
        if "\x00" in argument:
            raise ValueError(f"Command argument at index {index} contains a null byte.")
    # Validate that the first argument (the executable name) is not empty or whitespace.
    if not command[0].strip():
        raise ValueError("Executable name cannot be empty.")


def validate_timeout(timeout: int | float | None) -> None:
    """Validate the optional command timeout.

    Args:
        timeout: Maximum execution time in seconds, or None for no timeout.

    Raises:
        TypeError: If the timeout is not an integer, float, or None.
        ValueError: If the timeout is non-finite or not positive.
    """
    # If timeout is None, we consider it valid and return early.
    if timeout is None:
        return

    # Validate that the timeout is a number (int or float) and not a boolean.
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError("Timeout must be an int, float, or None.")

    # Validate that the timeout is finite and positive.
    try:
        is_finite = math.isfinite(timeout)
    except OverflowError:
        is_finite = False

    if not is_finite:
        raise ValueError("Timeout must be finite.")

    # Validate that the timeout is greater than zero.
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")


def _normalize_output(output: str | bytes | None) -> str:
    """Normalize captured process output to a string.

    Args:
        output: Captured output, which may be a string, bytes, or None.

    Returns:
        A string representation of the output, with bytes decoded to UTF-8
        and None converted to an empty string. Any decoding errors are
        replaced with the Unicode replacement character.

    """
    if output is None:
        return ""

    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")

    return output


def run_command(
    command: Sequence[str],
    *,
    timeout: int | float | None = None,
) -> CommandResult:
    """Execute an external command and return its result.

    Args:
        command: Executable name followed by its arguments.
        timeout: Maximum execution time in seconds, or None for no timeout.

    Returns:
        A result describing the command execution, including its status,
        captured output, duration, and any execution error.

    Raises:
        TypeError: If the command or timeout has an invalid type.
        ValueError: If the command or timeout has an invalid value.
    """
    validate_command(command)
    validate_timeout(timeout)

    normalized_command = tuple(command)
    # Record the start time to measure execution duration.
    start_time = time.perf_counter()

    # Prepare a human-readable description of the timeout for logging purposes.
    # If timeout is None, we indicate that there is no timeout.
    # Use a concise, consistent timeout description in logs.
    timeout_description = f"{timeout}s" if timeout is not None else "unlimited"

    logger.debug(
        "Executing command: command=%r, timeout=%s",
        normalized_command,
        timeout_description,
    )

    try:
        completed = subprocess.run(  # noqa: S603
            normalized_command,
            capture_output=True,
            text=True,
            encoding="utf-8",  # Ensure consistent UTF-8 encoding for captured output.
            errors="replace",  # # Replace invalid UTF-8 characters.
            check=False,
            timeout=timeout,
            shell=False,
        )

    except subprocess.TimeoutExpired as exc:
        # TimeoutExpired may contain partial output as bytes, even with
        # text=True, so normalize both streams before storing the result.
        result = CommandResult(
            command=normalized_command,
            status=CommandStatus.TIMED_OUT,
            returncode=None,
            stdout=_normalize_output(exc.stdout),
            stderr=_normalize_output(exc.stderr),
            duration_seconds=time.perf_counter() - start_time,
            error=f"Command timed out after {timeout} seconds.",
        )

        logger.warning(
            "Command timed out: command=%r, timeout=%s, duration=%.2fs",
            normalized_command,
            f"{timeout}s" if timeout is not None else "unlimited",
            result.duration_seconds,
        )

        return result

    except FileNotFoundError as exc:
        # The executable could not be found at process startup.
        result = CommandResult(
            command=normalized_command,
            status=CommandStatus.NOT_FOUND,
            returncode=None,
            stdout="",
            stderr="",
            duration_seconds=time.perf_counter() - start_time,
            error=str(exc),
        )

        logger.error(
            "Command not found: command=%r, error=%r",
            normalized_command,
            result.error,
        )

        return result

    except PermissionError as exc:
        # The operating system denied permission to start the process.
        result = CommandResult(
            command=normalized_command,
            status=CommandStatus.PERMISSION_DENIED,
            returncode=None,
            stdout="",
            stderr="",
            duration_seconds=time.perf_counter() - start_time,
            error=str(exc),
        )

        logger.error(
            "Command execution failed: command=%r, error=%r",
            normalized_command,
            result.error,
        )

        return result

    except OSError as exc:
        # Handle other operating-system errors raised during process startup.
        result = CommandResult(
            command=normalized_command,
            status=CommandStatus.EXECUTION_ERROR,
            returncode=None,
            stdout="",
            stderr="",
            duration_seconds=time.perf_counter() - start_time,
            error=str(exc),
        )

        logger.error(
            "Command execution failed: command=%r, error=%r",
            normalized_command,
            result.error,
        )

        return result

    # A non-zero exit code indicates command failure; stderr alone does not.
    status = (
        CommandStatus.SUCCESS if completed.returncode == 0 else CommandStatus.FAILED
    )

    result = CommandResult(
        command=normalized_command,
        status=status,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        duration_seconds=time.perf_counter() - start_time,
        error=(
            completed.stderr.strip() or "Command exited with a non-zero code"
            if completed.returncode != 0
            else None
        ),
    )

    if result.success:
        logger.debug(
            "Command completed: command=%r, duration=%.2fs",
            normalized_command,
            result.duration_seconds,
        )
    else:
        logger.debug(
            "Command failed: command=%r, returncode=%d, duration=%.2fs, error=%r",
            normalized_command,
            result.returncode,
            result.duration_seconds,
            result.error,
        )

    return result
