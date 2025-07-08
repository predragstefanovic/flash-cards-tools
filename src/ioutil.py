import logging
import os
from typing import Generator
from typing import NamedTuple


class Line(NamedTuple):
    contents: str
    bytes: int

def read_lines(filepath:str) -> Generator[Line, None, None]:
    try:
        with open(filepath, "r", encoding="utf-8") as fi:
            for line in fi:
                bytes = len(line.encode("utf-8"))
                yield Line(contents=line.strip(), bytes=bytes)
    except FileNotFoundError:
        logging.error(f"Input file not found at '{filepath}'")
        # This will cause the generator to stop immediately
        return

def get_file_size(filepath: str) -> int:
    return os.path.getsize(filepath)