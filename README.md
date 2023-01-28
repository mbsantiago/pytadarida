# PyTadarida

[![Tests](https://github.com/mbsantiago/pytadarida/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/mbsantiago/pytadarida/actions/workflows/unit-tests.yml)
[![Pylint](https://github.com/mbsantiago/pytadarida/actions/workflows/pylint.yml/badge.svg)](https://github.com/mbsantiago/pytadarida/actions/workflows/pylint.yml)
[![PyPI](https://github.com/mbsantiago/pytadarida/actions/workflows/python-publish.yml/badge.svg)](https://github.com/mbsantiago/pytadarida/actions/workflows/python-publish.yml)

PyTadarida is a Python wrapper for the Tadarida-D algorithm, which is a method
for detecting presence of bioacoustic events in audio recordings. The algorithm
is described in detail in the following paper:

> Bas, Y., Bas, D., & Julien, J.-F. (2017). Tadarida: A Toolbox for Animal
> Detection on Acoustic Recordings. Journal of Open Research Software, 5(1), 6.
> DOI: http://doi.org/10.5334/jors.154

The original implementation of the algorithm is written in C++, and is available
on its [GitHub repository](https://github.com/YvesBas/Tadarida-D).

## Installation

PyTadarida only runs in Linux. Make sure you have all the Tadarida-D
dependencies, in Ubuntu you can install them with

    sudo apt-get install libfftw3-dev libicu-dev libsndfile1-dev libqt5core5a

PyTadarida is available on PyPI, and can be installed with pip:

    pip install pytadarida

## Usage

PyTadarida exposes a single function, `run_tadarida`, which takes a list of .wav
files or directories containing .wav files as input, and returns a pandas
DataFrame containing the detected events.

```python
    from pytadarida import run_tadarida

    events, status = run_tadarida(["/path/to/file.wav", "/path/to/directory"])
```

The `status` variable is an object containing the status of the algorithm after
running. It can generally ignored, but can be useful to check whether the
algorithm was able to process the file, and any warnings that were generated.

```python
    # The stdout attribute contains what the algorithm prints to the
    # console while running
    tadarida_run_message = status.stdout

    # The errors attribute contains any errors that were generated while
    # running the algorithm
    tadarida_error_message = status.errors

    # The detect attribute contains the detection log of the algorithm
    tadarida_detection_message = status.detect
```

## License

As the original Tadarida-D algorithm is licensed under the GNU General Public
License v3.0, PyTadarida is also licensed under the GNU General Public License
v3.0. This means that PyTadarida is free software, and you are free to use,
modify, and redistribute it under certain conditions. See the LICENSE file for
more information.

## Contributing

Contributions are welcome! If you find a bug, or have a feature request, please
open an issue on the
[GitHub repository](https://github.com/mbsantiago/pytadarida)
