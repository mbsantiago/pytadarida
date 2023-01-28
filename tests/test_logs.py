"""Test pytadarida logs module."""

import os
import shutil
from pathlib import Path

import pytest

from pytadarida import logs


@pytest.fixture(autouse=True)
def clean_log_dir():
    """Clean the log directory."""
    if Path("log").exists():
        shutil.rmtree("log")

    # Create empty log dir
    Path("log").mkdir()

    yield

    if Path("log").exists():
        shutil.rmtree("log")


def test_read_error_log():
    """Test read_errors function."""
    with open("log/error.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    errors = logs.read_error_log()

    assert errors == "test"


def test_read_detect_log():
    """Test read_detect_log function."""
    with open("log/detec.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    detect_log = logs.read_detect_log()

    assert detect_log == "test"


def test_read_tadarida_log():
    """Test read_tadarida_log function."""
    with open("log/tadaridaD.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    tadarida_log = logs.read_tadarida_log()

    assert tadarida_log == "test"


def test_read_error_log_returns_empty_string_if_not_exists():
    """Test read_errors function returns empty string if log does not exist."""
    if Path("log/error.log").exists():
        os.remove("log/error.log")

    errors = logs.read_error_log()

    assert errors == ""


def test_read_detect_log_returns_empty_string_if_not_exists():
    """Test read_detect_log function returns empty string if log does not exist."""
    if Path("log/detec.log").exists():
        os.remove("log/detec.log")

    detect_log = logs.read_detect_log()

    assert detect_log == ""


def test_read_tarida_log_returns_empty_string_if_not_exists():
    """Test read_tadarida_log function returns empty string if log does not exist."""
    if Path("log/tadaridaD.log").exists():
        os.remove("log/tadaridaD.log")

    tadarida_log = logs.read_tadarida_log()

    assert tadarida_log == ""


def test_logs_are_cleaned():
    """Test logs are cleaned."""
    with open("log/error.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    with open("log/detec.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    with open("log/tadaridaD.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    logs.clean_logs()

    assert not os.path.exists("log/error.log")
    assert not os.path.exists("log/detec.log")
    assert not os.path.exists("log/tadaridaD.log")


def test_clean_logs_does_not_raise_if_log_dir_does_not_exist():
    """Test clean_logs does not raise if log dir does not exist."""
    if Path("log").exists():
        shutil.rmtree("log")

    logs.clean_logs()


def test_clean_logs_does_not_raise_if_log_dir_is_empty():
    """Test clean_logs does not raise if log dir is empty."""
    logs.clean_logs()


def test_clean_logs_remove_log_dir_if_empty_after_deleting_logs():
    """Test clean_logs removes log dir if empty after deleting logs."""
    with open("log/error.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    logs.clean_logs()

    assert not os.path.exists("log")


def test_clean_logs_does_not_remove_if_log_dir_is_not_empty():
    """Test clean_logs does not remove log dir if not empty."""
    with open("log/error.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    # create a file in the log dir that is not a log file
    with open("log/test.txt", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    logs.clean_logs()

    assert os.path.exists("log")

    # remove the file created in the test
    # so that the test can be run again
    os.remove("log/test.txt")


def test_get_run_status_returns_run_status():
    """Test get_run_status returns run status."""
    # Write test text to log files
    with open("log/tadaridaD.log", "w", encoding="utf-8") as logfile:
        logfile.write("test")

    with open("log/detec.log", "w", encoding="utf-8") as logfile:
        logfile.write("detect")

    with open("log/error.log", "w", encoding="utf-8") as logfile:
        logfile.write("error")

    run_status = logs.get_run_status()

    # Check that the run status is a RunStatus object
    # containing the correct values in the correct attributes
    # and that the logs are cleaned
    assert run_status.stdout == "test"
    assert run_status.detect == "detect"
    assert run_status.error == "error"
    assert not os.path.exists("log/tadaridaD.log")
    assert not os.path.exists("log/detec.log")
    assert not os.path.exists("log/error.log")
