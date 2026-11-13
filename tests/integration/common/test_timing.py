"""Integration tests for the timing module."""

import time

import pytest

from local_ai_platform.common.timing import Timer

pytestmark = pytest.mark.integration


def test_timer_measures_operation_duration() -> None:
    """Verify that the timer measures an operation's duration."""
    timer = Timer()

    timer.start()
    time.sleep(0.1)
    timer.stop()

    assert timer.end_time > timer.start_time
    assert timer.duration_seconds >= 0.1
    assert timer.duration_minutes == timer.duration_seconds / 60.0


def test_timer_supports_consecutive_measurements() -> None:
    """Verify that the timer supports consecutive measurements."""
    timer = Timer()

    timer.start()
    time.sleep(0.05)
    timer.stop()

    first_duration = timer.duration_seconds

    timer.start()
    time.sleep(0.1)
    timer.stop()

    second_duration = timer.duration_seconds

    assert first_duration >= 0.05
    assert second_duration >= 0.1
    assert timer.start_time < timer.end_time


def test_timer_returns_minutes_for_short_operation() -> None:
    """Verify minute conversion for a short operation."""
    timer = Timer()

    timer.start()
    time.sleep(0.001)
    timer.stop()

    assert timer.duration_seconds > 0.0
    assert timer.duration_minutes > 0.0
    assert timer.duration_minutes == timer.duration_seconds / 60.0
