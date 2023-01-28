"""Test tadarida output module.

The Tadarida-D binary outputs a file for each processed audio file. The
output file is located in a subdirectory of the input directory. The
subdirectory is named "txt" and the output file has the same name as the
input file but with the extension ".ta".

This module tests the functions that:

1. get the output files from the input files.
2. parses the output files into python objects.
3. writes the python objects to a .ta file.
4. writes the python objects to a .csv file.
5. clean up the output files.
"""
from pathlib import Path

import pytest

from pytadarida import output


def test_get_output_files(tmp_path: Path) -> None:
    """Test get_output_files function."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()

        file.touch()

    # Test
    assert output.get_output_files(input_files) == output_files


def test_get_output_files_raises_with_missing_output(tmp_path: Path) -> None:
    """Test get_output_files raises with missing output."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Test
    with pytest.raises(FileNotFoundError):
        output.get_output_files(input_files)


def test_get_output_files_on_directory(tmp_path: Path) -> None:
    """Test get_output_files on directory."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Test
    assert output.get_output_files([tmp_path]) == output_files


def test_get_output_files_on_mixed_inputs(tmp_path: Path) -> None:
    """Test get_output_files on mixed inputs."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "subdir" / "file2.wav",
        tmp_path / "subdir" / "file3.wav",
    ]

    for file in input_files:
        if file.parent != tmp_path and not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Test
    assert (
        output.get_output_files([input_files[0], input_files[1].parent])
        == output_files
    )


def test_clean_output_files(tmp_path: Path) -> None:
    """Test clean_output_files function."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Test
    output.clean_output_files(input_files)
    for file in output_files.values():
        assert not file.exists()


def test_clean_output_files_does_not_delete_wav_files(tmp_path: Path) -> None:
    """Test clean_output_files does not delete wav files."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Test
    output.clean_output_files(input_files)
    for file in input_files:
        assert file.exists()


def test_clean_output_files_does_not_delete_non_ta_files(
    tmp_path: Path,
) -> None:
    """Test clean_output_files does not delete non-ta files."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Create non-ta files
    non_ta_files = {
        path: path.parent / "txt" / f"{path.stem}.txt" for path in input_files
    }

    for file in non_ta_files.values():
        if not file.parent.exists():
            file.parent.mkdir()

        file.touch()

    # Test
    output.clean_output_files(input_files)
    for file in non_ta_files.values():
        assert file.exists()


def test_clean_output_deletes_txt_dir_when_empty(tmp_path: Path) -> None:
    """Test clean_output deletes txt dir when empty."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()

        file.touch()

    # Test
    output.clean_output_files(input_files)
    for file in output_files.values():
        assert not file.parent.exists()


def test_clean_output_does_not_delete_txt_dir_if_not_empty(
    tmp_path: Path,
) -> None:
    """Test clean_output does not delete txt dir if not empty."""
    # Create input files
    input_files = [
        tmp_path / "file1.wav",
        tmp_path / "file2.wav",
        tmp_path / "file3.wav",
    ]

    for file in input_files:
        file.touch()

    # Create output files
    output_files = {
        path: path.parent / "txt" / f"{path.stem}.ta" for path in input_files
    }

    for file in output_files.values():
        if not file.parent.exists():
            file.parent.mkdir()

        file.touch()

    # Create non-ta files
    non_ta_files = {
        path: path.parent / "txt" / f"{path.stem}.txt" for path in input_files
    }

    for file in non_ta_files.values():
        if not file.parent.exists():
            file.parent.mkdir()
        file.touch()

    # Test
    output.clean_output_files(input_files)
    for file in non_ta_files.values():
        assert file.parent.exists()


def test_parse_ta_file_has_correct_output(tmp_path: Path) -> None:
    """Test parse_ta_file has correct output."""
    # Create input file
    input_file = tmp_path / "file1.ta"
    input_file.touch()
