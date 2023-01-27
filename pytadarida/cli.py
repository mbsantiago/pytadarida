import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        metavar="FILES",
        type=str,
        nargs="+",
        help="File, or files, to process with tadarida",
    )
    parser.add_argument(
        "--threads",
        "-t",
        metavar="T",
        type=int,
        default=1,
        help="Number of CPU threads to use for file processing.",
    )
    parser.add_argument(
        "--time-expansion",
        "-e",
        metavar="E",
        type=float,
        default=1,
        help="Time expansion factor of the recordings to process.",
    )
    parser.add_argument(
        "--version",
        "-v",
        metavar="V",
        type=int,
        choices=[1, 2],
        default=1,
        help=(
            "Version of tadarida to use. Version 2 has an "
            "expanded set of call parameters available."
        ),
    )
    parser.add_argument(
        "--frequency-band",
        "-f",
        metavar="F",
        type=int,
        choices=[1, 2],
        default=1,
        help=(
            "Frequency band in which to search for bat calls. "
            "Using band 1 will search for calls at low frequencies "
            "(0.8 to 25 kHz) while band 2 will detect calls in the "
            "8 to 250 kHz range."
        ),
    )
    parser.add_argument(
        "--save",
        "-s",
        action="store_true",
        help=("If present, the output of tadarida will be stored in a tsv file."),
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        metavar="O",
        type=str,
        default="txt",
        help=(
            "Directory in which to store the outputs of tadarida. "
            "Paths are relative to the location of the processed files."
        ),
    )
    parser.add_argument(
        "--compression",
        "-c",
        action="store_true",
        help="If present, the output files will be compressed.",
    )
    return parser.parse_args()
