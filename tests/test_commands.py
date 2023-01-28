"""Tests for pytadarida.commands"""
from pathlib import Path

import pandas as pd
import pytest

from pytadarida.commands import run_tadarida
from pytadarida.logs import RunStatus

DATA_DIR = Path(__file__).parent / "data"

TEST_WAV = DATA_DIR / "Barbastella_barbastellus_1_s.wav"
TEST_TA = DATA_DIR / "ta_file_version_1.ta"
TEST_DIR_WAVS = DATA_DIR / "dir_of_wavs"


def test_run_tadarida_works_on_wav_file():
    """Test run_tadarida works on a wav file."""
    assert TEST_WAV.exists()
    run_tadarida(TEST_WAV)


def test_run_tadarida_fails_on_non_existing_file():
    """Test run_tadarida fails on a non existing file."""
    test_file = DATA_DIR / "non_existing_file.wav"
    assert not test_file.exists()
    with pytest.raises(FileNotFoundError):
        run_tadarida(test_file)


def test_run_tadarida_fails_on_non_wav_file():
    """Test run_tadarida fails on a non-wav file."""
    assert TEST_TA.exists()
    with pytest.raises(ValueError):
        run_tadarida(TEST_TA)


def test_run_tadarida_return_type():
    """Test run_tadarida returns the detection dataframe and runstatus"""
    assert TEST_WAV.exists()
    detections, status = run_tadarida(TEST_WAV)
    assert isinstance(detections, pd.DataFrame)
    assert isinstance(status, RunStatus)


def test_run_tadarida_works_on_dir_of_wavs():
    """Test run_tadarida works on a dir of wav files."""
    assert TEST_DIR_WAVS.exists()
    run_tadarida(TEST_DIR_WAVS)


def test_no_log_files_after_run_tadarida():
    """Test that no log files are created after running tadarida."""
    assert TEST_WAV.exists()
    run_tadarida(TEST_WAV)
    assert not any(Path("log").glob("*.log"))


def test_output_files_are_cleared_after_run_tadarida():
    """Test that output files are cleared after running tadarida."""
    assert TEST_WAV.exists()
    run_tadarida(TEST_WAV)
    assert not (TEST_WAV.parent / "txt").exists()
