import json

from pytadarida.cli import parse_arguments
from pytadarida.tadarida import run_tadarida


if __name__ == "__main__":
    args = parse_arguments()
    output = run_tadarida(
        files=args.files,
        threads=args.threads,
        time_expansion=args.time_expansion,
        features=args.version,
        frequency_band=args.frequency_band,
        compression=args.compression,
        save=args.save,
        output_dir=args.output_dir,
    )
    print(json.dumps(output, indent=2))
