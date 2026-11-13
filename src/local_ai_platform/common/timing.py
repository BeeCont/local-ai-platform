"""Common timing utilities for measuring execution duration of operations."""

import time


class Timer:
    """Measure the executtion duration of an operation."""

    def __init__(self) -> None:
        """Initialize the timer."""
        self._start_time: float | None = None
        self._end_time: float | None = None

    def start(self) -> None:
        """Start or restart the timer."""
        if self._start_time is not None and self._end_time is None:
            raise RuntimeError("Timer has already been started.")

        self._start_time = time.perf_counter()
        self._end_time = None

    def stop(self) -> None:
        """Stop the timer and record the end time."""
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")

        if self._end_time is not None:
            raise RuntimeError("Timer has already been stopped.")

        self._end_time = time.perf_counter()

    @property
    def start_time(self) -> float:
        """Get the start time of the timer.

        Returns:
            The start time in seconds since the epoch.
        """
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        return self._start_time

    @property
    def end_time(self) -> float:
        """Get the end time of the timer.

        Returns:
            The end time in seconds since the epoch.
        """
        if self._end_time is None:
            raise RuntimeError("Timer has not been stopped.")
        return self._end_time

    @property
    def duration_seconds(self) -> float:
        """Get the duration in seconds between start and stop.

        Returns:
            The duration in seconds.
        """
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        if self._end_time is None:
            raise RuntimeError("Timer has not been stopped.")

        return self._end_time - self._start_time

    @property
    def duration_minutes(self) -> float:
        """Get the duration in minutes between start and stop.

        Returns:
            The duration in minutes.
        """
        return self.duration_seconds / 60.0
