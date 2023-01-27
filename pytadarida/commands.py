import subprocess

from pytadarida.configs import TADARIDA_BINARY


def _run_command(*args, capture_output=False):
    result = subprocess.run(
        [TADARIDA_BINARY, *args],
        capture_output=capture_output,
    )
    return result.stdout


def command_help():
    return _run_command("-h").decode("utf-8")


def _build_args(
    threads=1,
    time_expansion=1,
    features=2,
    frequency_band=1,
    compression=False,
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

    if compression:
        args.append("-c")

    return args


def run_tadarida_binary(
    files,
    threads=1,
    time_expansion=1,
    features=2,
    frequency_band=1,
    compression=False,
):
    if not isinstance(files, (list, tuple)):
        files = [files]

    args = _build_args(
        threads=threads,
        time_expansion=time_expansion,
        features=features,
        frequency_band=frequency_band,
        compression=compression,
    )

    args = [*args, *files]
    return _run_command(*args, capture_output=True)
