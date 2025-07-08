import logging
from typing import Generator

def read_lines(filepath:str) -> Generator[str, None, None]:

    try:
        with open(filepath, "r", encoding="utf-8") as fi:
            for line in fi:
                yield line.strip()
    except FileNotFoundError:
        logging.error(f"Input file not found at '{filepath}'")
        # This will cause the generator to stop immediately
        return
