"""Parsing functions for .ta files."""
import os
from typing import Dict, Union
from pathlib import Path

import pandas as pd

PathLike = Union[str, os.PathLike]


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
    dataframe = pd.read_csv(str(path), sep="\t")

    # Check that the output is a dataframe
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The output is not a pandas dataframe.")

    return dataframe


def parse_detections(mapping: Dict[Path, Path]) -> pd.DataFrame:
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
