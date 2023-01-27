from pytadarida.commands import run_tadarida_binary
from pytadarida.output import get_output
from pytadarida.output import clean_output
from pytadarida.output import move_output


def run_tadarida(
    files,
    threads=1,
    time_expansion=1,
    features=2,
    frequency_band=1,
    compression=False,
    save=False,
    output_dir="txt/",
):
    if compression:
        raise NotImplementedError

    if not isinstance(files, (list, tuple)):
        files = [files]

    run_tadarida_binary(
        files,
        threads=threads,
        time_expansion=time_expansion,
        features=features,
        frequency_band=frequency_band,
        compression=compression,
    )

    output = get_output(files, compression=compression)

    if not save:
        clean_output(files)

    else:
        move_output(files)

    return output
