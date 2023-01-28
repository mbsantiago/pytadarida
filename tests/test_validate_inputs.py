"""Tests for pytadarida.validate_inputs module.

This module tests the pytadarida.validate_inputs module.

"""
import pytest

from pytadarida.validate_inputs import validate_files


def test_validate_files_works_on_wav_file(tmp_path):
    test_file = tmp_path / "test.wav"
    test_file.touch()
    assert test_file.exists()
    validate_files([test_file])

    test_file = tmp_path / "test.WAV"
    test_file.touch()
    assert test_file.exists()
    validate_files([test_file])


def test_validate_files_fails_on_non_existing_file(tmp_path):
    test_file = tmp_path / "test.wav"
    assert not test_file.exists()
    with pytest.raises(FileNotFoundError):
        validate_files([test_file])


def test_validate_files_fails_on_non_wav_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.touch()
    assert test_file.exists()
    with pytest.raises(ValueError):
        validate_files([test_file])


def test_validate_files_works_on_directory_of_wav_files(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    test_file = test_dir / "test.wav"
    test_file.touch()
    assert test_dir.exists()
    validate_files([test_dir])


def test_validate_files_fails_on_non_existing_directory(tmp_path):
    test_dir = tmp_path / "test_dir"
    assert not test_dir.exists()
    with pytest.raises(FileNotFoundError):
        validate_files([test_dir])
