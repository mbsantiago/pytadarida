"""PyTadarida: A Python package for Tadarida.

PyTadarida is a Python package for Tadarida-D, a tool for the extraction of
sound events from wav files. It is based on the Tadarida-D tool developed by
Yves Bas. The original Tadarida-D tool is available at

https://github.com/YvesBas/Tadarida-D

PyTadarida is distributed under the GNU Lesser General Public License v3.0.


Functions
---------
run_tadarida
    Run Tadarida-D on a list of .wav files or a directory containing .wav
    files.

Classes
-------
RunStatus
    A class to store the status of a Tadarida-D run.
"""

from pytadarida.commands import run_tadarida
from pytadarida.logs import RunStatus

__version__ = "0.1.0"


__all__ = [
    "run_tadarida",
    "RunStatus",
    "__version__",
]
