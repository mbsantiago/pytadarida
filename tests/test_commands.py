from pytadarida.commands import command_help
from pytadarida.commands import run_tadarida


def test_command_help_tadarida():
    help = command_help()
    print(help)
    assert help
    assert False


def test_run_tadarida():
    file = "/home/santiago/Datasets/lib_chiroptera/5aa403e95d5b148aa61389a3.WAV"
    results = run_tadarida(file)

    print(results)

    assert False
