"""Run the tadarida binary on the given files.

This module contains the run_tadarida function, which runs the tadarida binary
on the given files.

"""
import os
import subprocess
from typing import Iterable, List, Literal, Tuple, Union

import pandas as pd

from pytadarida.configs import TADARIDA_BINARY
from pytadarida.logs import RunStatus, get_run_status
from pytadarida.output import clean_output_files, get_output_files
from pytadarida.parsing import parse_detections
from pytadarida.validate_inputs import validate_files

__all__ = [
    "run_tadarida",
]


PathLike = Union[str, os.PathLike]


def _run_command(*args: str, capture_output: bool = False):
    result = subprocess.run(
        [TADARIDA_BINARY, *args],
        capture_output=capture_output,
        check=True,
    )
    return result.stdout


def _build_args(
    threads=1,
    time_expansion=1,
    features=2,
    frequency_band=1,
):
    args = [
        "-t",
        str(threads),
        "-x",
        str(time_expansion),
        "-v",
        str(features),
        "-f",
        str(frequency_band),
    ]

    return args


def run_tadarida(
    files: Union[
        PathLike, List[PathLike], Tuple[PathLike, ...], Iterable[PathLike]
    ],
    threads: int = 1,
    time_expansion: Literal[10, 1] = 1,
    features=2,
    frequency_band: Literal[1, 2] = 1,
) -> Tuple[pd.DataFrame, RunStatus]:
    """Run the tadarida binary on the given files.

    Will run the tadarida binary on the given files, and return a dataframe
    with the detected sound events.

    Parameters
    ----------
    files : str or list of str
        Either a directory path containing .wav files or a list of .wav files,
        to be processed. Relative or absolute paths can be used. Audio files
        must be short. Accepted limit depends on sound file characteristics
        (between 6.4 and 12.8 seconds in high frequency (HF) mode, and between
         32 and 64 seconds in low frequency (LF) mode).
    threads : int, optional
        Allows to execute n parallel threads (1 by default).
        Note that 1 thread consumes approximately 150 MB of memory.
    time_expansion : float, optional
        Time expansion factor, either 10 (default) for 10-times expanded .wav
        files (most commonly used in bat monitoring) or 1 for direct
        recordings.
    features : int, optional
        sets the list of features to be extracted on each detected sound
        event.
    frequency_band : int, optional
        Frequency bands to be used; n = 2 allows to treat low frequencies
        (0.8 to 25 kHz) whereas n=1 (default) treats high frequencies
        (8 to 250 kHz).

    Returns
    -------
    detections: pd.DataFrame
        Dataframe with detected sound events.
    status: RunStatus
        A RunStatus object containing the stdout and stderr of the tadarida
        binary.

    Raises
    ------
    FileNotFoundError

    """
    if isinstance(files, (str, os.PathLike)):
        files = [files]

    validate_files(files)

    args = _build_args(
        threads=threads,
        time_expansion=time_expansion,
        features=features,
        frequency_band=frequency_band,
    )

    args = [*args, *files]

    _run_command(*args, capture_output=False)

    status = get_run_status()

    try:
        outputs = get_output_files(files)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "The tadarida binary did not produce any output files.\n"
            f"Tadarida-D Output: {status.stdout}\n"
            f"Error: {status.error}\n"
        ) from error

    try:
        detections = parse_detections(outputs)

        # Remove the output files after parsing
        clean_output_files(files)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "Error parsing the output files.\n"
            f"Tadarida-D Output: {status.stdout}\n"
            f"Error: {status.error}\n"
        ) from error

    return detections, status
