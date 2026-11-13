"""Unit tests for the timing module."""

from unittest.mock import patch

import pytest

from local_ai_platform.common.timing import Timer

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


def mock_time_perf_counter(*timestamps: float):
    """Patch time.perf_counter to return specified timestamps."""
    return patch("time.perf_counter", side_effect=timestamps)


def test_timer_start_and_stop_returns_values_as_float():
    """Test that start and stop store the expected timestamps."""
    with mock_time_perf_counter(1.0, 2.0):
        timer = Timer()
        timer.start()
        timer.stop()

    assert timer.start_time == 1.0
    assert timer.end_time == 2.0


def test_timer_get_start_time_without_start_raises_runtime_error():
    """Test that accessing start_time before start raises RuntimeError."""
    timer = Timer()
    with pytest.raises(RuntimeError):
        timer.start_time


def test_timer_get_end_time_without_stop_raises_runtime_error():
    """Test that accessing end_time before stop raises RuntimeError."""
    with mock_time_perf_counter(1.0):
        timer = Timer()
        timer.start()
        with pytest.raises(RuntimeError):
            timer.end_time


def test_timer_get_duration_seconds_returns_float():
    """Test that duration_seconds returns the expected duration."""
    with mock_time_perf_counter(1.0, 2.0):
        timer = Timer()
        timer.start()
        timer.stop()

    assert timer.duration_seconds == 1.0


def test_timer_get_duration_minutes_returns_float():
    """Test that duration_minutes returns the expected duration."""
    with mock_time_perf_counter(1.0, 61.0):
        timer = Timer()
        timer.start()
        timer.stop()

    assert timer.duration_minutes == 1.0


def test_timer_start_resets_previous_measurement():
    """Test that starting again resets the previous measurement."""
    with mock_time_perf_counter(1.0, 2.0, 3.0, 4.0):
        timer = Timer()
        timer.start()
        timer.stop()
        timer.start()
        timer.stop()

    assert timer.start_time == 3.0
    assert timer.end_time == 4.0


def test_timer_stop_without_start_raises_runtime_error():
    """Test that stop before start raises RuntimeError."""
    timer = Timer()
    with pytest.raises(RuntimeError):
        timer.stop()


def test_timer_duration_seconds_without_start_raises_runtime_error():
    """Test that duration_seconds before start raises RuntimeError."""
    timer = Timer()
    with pytest.raises(RuntimeError):
        timer.duration_seconds


def test_timer_duration_minutes_without_start_raises_runtime_error():
    """Test that duration_minutes before start raises RuntimeError."""
    timer = Timer()
    with pytest.raises(RuntimeError):
        timer.duration_minutes


def test_timer_duration_seconds_without_stop_raises_runtime_error():
    """Test that duration_seconds before stop raises RuntimeError."""
    with mock_time_perf_counter(1.0):
        timer = Timer()
        timer.start()
        with pytest.raises(RuntimeError):
            timer.duration_seconds


def test_timer_duration_minutes_without_stop_raises_runtime_error():
    """Test that duration_minutes before stop raises RuntimeError."""
    with mock_time_perf_counter(1.0):
        timer = Timer()
        timer.start()
        with pytest.raises(RuntimeError):
            timer.duration_minutes


def test_timer_new_start_without_stop_raises_runtime_error():
    """Test that starting again before stop raises RuntimeError."""
    with mock_time_perf_counter(1.0, 2.0):
        timer = Timer()
        timer.start()
        with pytest.raises(RuntimeError):
            timer.start()


def test_timer_new_stop_after_stop_raises_runtime_error():
    """Test that stopping again after stop raises RuntimeError."""
    with mock_time_perf_counter(1.0, 2.0):
        timer = Timer()
        timer.start()
        timer.stop()
        with pytest.raises(RuntimeError):
            timer.stop()


def test_timer_zero_duration():
    """Test that equal start and stop timestamps produce zero duration."""
    with mock_time_perf_counter(1.0, 1.0):
        timer = Timer()
        timer.start()
        timer.stop()

    assert timer.duration_seconds == 0.0
    assert timer.duration_minutes == 0.0
