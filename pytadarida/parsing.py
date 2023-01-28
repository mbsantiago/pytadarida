"""Parsing functions for .ta files."""
import os

import pandas as pd

PathLike = str | os.PathLike


__all__ = [
    "parse_ta_file",
    "parse_detections",
]


def parse_ta_file(path: PathLike) -> pd.DataFrame:
    """Parse a .ta file into a pandas dataframe.

    Parameters
    ----------
    path : str or os.PathLike

    Returns
    -------
    pd.DataFrame
        Dataframe with detected sound events.

    Raises
    ------
    FileNotFoundError

    """
    return pd.read_csv(path, sep="\t", header=0)


def parse_detections(mapping: dict[PathLike, PathLike]) -> pd.DataFrame:
    """Parse all .ta files in the given file mapping.

    The mapping is a dictionary of .wav files and their corresponding .ta
    files. Each .ta file is parsed into a pandas dataframe and returned
    as a single dataframe.

    Parameters
    ----------
    mapping : dict of str or os.PathLike
        Mapping of .wav files and their corresponding .ta files.

    Returns
    -------
    pd.DataFrame
        Dataframe with detected sound events.

    Raises
    ------
    FileNotFoundError

    """
    dfs = []
    for wav, ta_file in mapping.items():
        detections_df = parse_ta_file(ta_file)
        detections_df["wav"] = wav
        dfs.append(detections_df)
    return pd.concat(dfs, ignore_index=True)
