from typing import NamedTuple
from enum import Enum

class Language(str, Enum):
    GERMAN = "German"
    ENGLISH = "English"
    SERBIAN = "Serbian"

class Text(NamedTuple):
    contents: str
    language: Language

def ReadLine(filepath:str):
    with open(filepath) as fi:
        for line in fi:
            yield line.strip()
