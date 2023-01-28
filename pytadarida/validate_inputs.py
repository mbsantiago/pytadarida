"""Validate the input files.

This module contains functions to validate the input files.
"""
import os
from pathlib import Path
from typing import Iterable, List, Tuple, Union

PathLike = Union[str, os.PathLike]


__all__ = [
    "validate_files",
]


def _validate_single_path(path: PathLike) -> None:
    """Check that the given path is valid.

    If path is a directory, it must exist. If path is a file, it must exist
    and be a .wav file. If path is a directory and it does not exist, a
    FileNotFoundError is raised. If path is a file and it does not exist,
    a FileNotFoundError is raised. If path is a file and it is not a .wav
    file, a ValueError is raised.

    Parameters
    ----------
    path : str or os.PathLike
        A path to a file or directory. Relative or absolute paths can be used.

    Raises
    ------
    FileNotFoundError
        If the path does not exist.
    ValueError
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist.")

    if path.is_dir():
        return

    if path.suffix not in [".wav", ".WAV"]:
        raise ValueError(f"File {path} is not a .wav file.")


def validate_files(
    files: Union[List[PathLike], Tuple[PathLike], Iterable[PathLike]],
):
    """Check that the given files are valid.

    If files is a directory, it must exist and contain .wav files.
    If files is a list of files, they must exist and be .wav files.
    If files is a list of directories, they must exist and contain .wav files.
    If files is a list of both files and directories, they must all be valid.
    If not .wav files are found, a ValueError is raised.
    If it is a directory and it does not exist, a FileNotFoundError is raised.

    Parameters
    ----------
    files : list of str or os.PathLike
        Either a directory path containing .wav files or a list of .wav files,
        to be processed. Relative or absolute paths can be used.
    """
    if not files:
        raise ValueError("No files were given.")

    if isinstance(files, (str, os.PathLike)):
        files = [files]

    for file in files:
        if not isinstance(file, (str, os.PathLike)):
            raise TypeError(f"File {file} is not a valid type.")

        _validate_single_path(file)
