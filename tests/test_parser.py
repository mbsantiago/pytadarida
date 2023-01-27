import os
from pytadarida.parser import parse_ta_file


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_FILE = os.path.join(BASE_DIR, "txt/57843f7f016e730f14d3f5e7.ta")


def test_parse_ta_file():
    parsed = parse_ta_file(TEST_FILE)
    assert isinstance(parsed, list)
    assert isinstance(parsed[0], dict)
