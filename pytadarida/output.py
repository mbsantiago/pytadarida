"""
Parser module.

This module contains functions that parse the outputs of the
tadarida program into workable python objects.
"""
import csv
import os
import shutil
from typing import List

from dataclasses import dataclass


@dataclass
class DetectedSoundEvent:
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


def parse_ta_file(path: str, compression: bool = False):
    with open(path, "r") as ta_file:
        reader = csv.DictReader(ta_file, delimiter="\t")
        return list(reader)


def get_output_file(
    wav_file: str,
    output_dir: str = "txt",
    compression: bool = False,
) -> str:
    dirname = os.path.dirname(wav_file)
    basename = os.path.basename(wav_file)
    name, _ = os.path.splitext(basename)
    path = os.path.join(dirname, output_dir, f"{name}.ta")
    return path


def get_output(files: List[str], compression=False):
    results = []
    for filename in files:
        path = get_output_file(filename, compression=compression)
        results.extend(parse_ta_file(path, compression=compression))
    return results


def clean_output(files: List[str], compression: bool = False):
    for filename in files:
        output_file = get_output_file(filename, compression=compression)
        if os.path.exists(output_file):
            os.remove(output_file)

        directory = os.path.dirname(output_file)
        if not os.listdir(directory):
            os.rmdir(directory)


def move_output(files: List[str], output_dir: str = "txt", compression: bool = False):
    for filename in files:
        src = get_output_file(filename, compression=compression)
        dst = get_output_file(filename, output_dir=output_dir, compression=compression)

        if not os.path.exists(src):
            continue

        if src == dst:
            continue

        directory = os.path.dirname(dst)
        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.move(src, dst)

        src_dir = os.path.directory(src)
        if not os.listdir(src_dir):
            os.rmdir(src_dir)
