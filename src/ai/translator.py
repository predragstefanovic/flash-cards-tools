from abc import ABC, abstractmethod
from src.ai.types import Language, Text


class Translator(ABC):
    @abstractmethod
    def translate(self, original_text: Text, target_lang: Language) -> Text | None:
        """Translates text from a source language to a target language."""
        pass