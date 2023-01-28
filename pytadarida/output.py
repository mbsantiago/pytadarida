"""
Parser module.

This module contains functions that parse the outputs of the
tadarida program into workable python objects.
"""
import csv
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PathLike = str | os.PathLike


@dataclass
class DetectedSoundEvent:
    """DetectedSoundEvent object.

    Attributes
    ----------
    filename : str

    call_number : int

    version : int

    file_duration : float

    samplerate : int

    start_time : float

    duration : float

    previous_start : float

    min_freq : float

    max_freq : float

    band_width : float

    master_point_freq : float

    master_point_position : float

    maximum_energy_frequency : float

    """
    filename: str
    call_number: int
    version: int
    file_duration: float
    samplerate: int
    start_time: float
    duration: float
    previous_start: float
    min_freq: float
    max_freq: float
    band_width: float
    master_point_freq: float
    master_point_position: float
    maximum_energy_frequency: float


def parse_ta_file(path: PathLike) -> list[DetectedSoundEvent]:
    """Parse a .ta file into a list of DetectedSoundEvent objects.

    Parameters
    ----------
    path : str or os.PathLike

    Returns
    -------
    list of DetectedSoundEvent

    Raises
    ------
    FileNotFoundError

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")

    with open(path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        next(reader)  # skip header
        return [
            DetectedSoundEvent(
                filename=row[0],
                call_number=int(row[1]),
                version=int(row[2]),
                file_duration=float(row[3]),
                samplerate=int(row[4]),
                start_time=float(row[5]),
                duration=float(row[6]),
                previous_start=float(row[7]),
                min_freq=float(row[8]),
                max_freq=float(row[9]),
                band_width=float(row[10]),
                master_point_freq=float(row[11]),
                master_point_position=float(row[12]),
                maximum_energy_frequency=float(row[13]),
            )
            for row in reader
        ]


def get_wav_files(path: PathLike) -> list[Path]:
    """Get a list of all .wav files in the given directory.

    Parameters
    ----------
    path : str or os.PathLike

    Returns
    -------
    list of str or os.PathLike

    Raises
    ------
    FileNotFoundError

    """
    path = Path(path)
    return list(path.glob("**/*.[wW][aA][vV]"))


def get_output_files_from_path(
    path: PathLike,
) -> dict[PathLike, PathLike]:
    """Get a dictionary of all .wav files in the given directory and their
    corresponding .ta files.

    If path is a directory, it returns a dictionary of all .wav files in the
    directory and their corresponding .ta files.

    Parameters
    ----------
    path : str or os.PathLike

    Returns
    -------
    dict of str or os.PathLike

    Raises
    ------
    FileNotFoundError

    """
    path = Path(path)

    if path.is_file():
        target = path.parent / "txt" / f"{path.stem}.ta"

        if not target.exists():
            raise FileNotFoundError(f"File {target} does not exist.")

        return {path: target}

    wav_files = get_wav_files(path)

    ret = {}
    for wav_file in wav_files:
        target = wav_file.parent / "txt" / f"{wav_file.stem}.ta"

        if not target.exists():
            raise FileNotFoundError(f"File {target} does not exist.")

        ret[wav_file] = target

    return ret


def get_output_files(
    files: tuple[PathLike] | list[PathLike] | Iterable[PathLike],
) -> dict[PathLike, PathLike]:
    """Get a dictionary of all .wav files in the given list and their
    corresponding .ta files.

    Parameters
    ----------
    files : list of str or os.PathLike

    Returns
    -------
    dict of str or os.PathLike

    Raises
    ------
    FileNotFoundError

    """
    output_files = {}
    for filename in files:
        output_files.update(get_output_files_from_path(filename))
    return output_files


def clean_output(files: Iterable[PathLike]):
    """Clean the output files.

    Tadarida-D creates a subdirectory named "txt" in the directory of each
    processed audio file. The subdirectory contains a .ta file with the same
    name as the audio files. This function deletes the associated .ta files
    but nothing else. This function does not delete the audio file. If the
    "txt" directory is empty after deleting the .ta files, it is also deleted.

    Parameters
    ----------
    files : list of str or os.PathLike
        A file can be a wav file or a directory. If it is a directory, all
        corresponding .ta files to the .wav files in the directory are deleted.
    """
    output_files = get_output_files(files)
    for ta_file in output_files.values():
        ta_file = Path(ta_file)
        os.remove(ta_file)
        if not list(ta_file.parent.glob("*")):
            shutil.rmtree(ta_file.parent)
