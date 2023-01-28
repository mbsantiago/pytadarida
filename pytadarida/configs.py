"""
Configuration file for pytadarida.

This file contains the path to the TadaridaD binary, as well as the
default values for the command line arguments.

"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
"""The base directory of pytadarida."""

TADARIDA_BINARY = os.path.join(BASE_DIR, "TadaridaD", "TadaridaD")
"""The path to the TadaridaD binary."""
