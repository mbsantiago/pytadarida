"""Module for managing tadarida logs.

This module contains functions for reading and cleaning tadarida logs.

When Tadarida-D runs it produces three log files. These are:

- tadaridaD.log: This is the input log file. It contains the text printed
to the stdout by the tadarida binary.

- error.log: This is the error log file. It contains information about any
errors that occurred during the processing of the files.

- detect.log: This is the detection log file. It contains information about
the detected sound events and any internal processing info.

The log files are stored in a "log" directory at the current working directory.
"""
import os
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "clean_logs",
    "get_run_status",
]


LOG_DIR = Path("log")
STDOUT_LOG = LOG_DIR / "tadaridaD.log"
ERROR_LOG = LOG_DIR / "error.log"
DETECT_LOG = LOG_DIR / "detec.log"


@dataclass
class RunStatus:
    """Class for storing the status of a run.

    Attributes:
        stdout: The contents of the tadarida log file.
        error: The contents of the error log file.
        detect: The contents of the detection log file.
    """

    stdout: str
    error: str
    detect: str


def read_error_log() -> str:
    """Read the error log file.

    Returns:
        The contents of the error log file. If the file does not exist,
        an empty string is returned.
    """
    if not ERROR_LOG.exists():
        return ""

    with open(ERROR_LOG, "r", encoding="utf-8") as logfile:
        error_log = logfile.read()

    return error_log


def read_detect_log() -> str:
    """Read the detection log file.

    Returns:
        The contents of the detection log file. If the file does not exist,
        an empty string is returned.
    """
    if not DETECT_LOG.exists():
        return ""

    with open(DETECT_LOG, "r", encoding="utf-8") as logfile:
        detect_log = logfile.read()

    return detect_log


def read_tadarida_log() -> str:
    """Read the tadarida log file.

    Returns:
        The contents of the tadarida log file. If the file does not exist,
        an empty string is returned.
    """
    if not STDOUT_LOG.exists():
        return ""

    with open(STDOUT_LOG, "r", encoding="utf-8") as logfile:
        tadarida_log = logfile.read()

    return tadarida_log


def get_run_status() -> RunStatus:
    """Get the status of a run.

    Clears the log files after reading them.

    Returns:
        A RunStatus object containing the contents of the log files.
    """
    tadarida_log = read_tadarida_log()
    error_log = read_error_log()
    detect_log = read_detect_log()

    clean_logs()

    return RunStatus(tadarida_log, error_log, detect_log)


def clean_logs():
    """Remove the log files.

    Does not raise errors if the log files do not exist. Deletes the log
    dir if empty after removing the log files.
    """
    log_dir = Path("log")

    if not log_dir.exists():
        return

    for log_file in [STDOUT_LOG, ERROR_LOG, DETECT_LOG]:
        log_file.unlink(missing_ok=True)

    if not os.listdir(log_dir):
        log_dir.rmdir()
