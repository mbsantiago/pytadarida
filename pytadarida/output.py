"""
This module contains functions to get the output files of Tadarida-D.

Tadarida-D creates a subdirectory named "txt" in the directory of each
processed audio file. The subdirectory contains a .ta file with the same
name as the audio files. This module provides functions to get the
corresponding .ta files from a given audio file or a directory of audio
files.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Union

PathLike = Union[str, os.PathLike]


__all__ = [
    "get_output_files",
    "clean_output_files",
]


def get_wav_files(path: PathLike) -> List[Path]:
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
) -> Dict[Path, Path]:
    """Get a dictionary of .wav files to their corresponding .ta files.

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
    files: Union[Tuple[PathLike, ...], List[PathLike], Iterable[PathLike]],
) -> Dict[Path, Path]:
    """Get dictionary of .wav files in the given list and their .ta files.

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


def clean_output_files(files: Iterable[PathLike]):
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
