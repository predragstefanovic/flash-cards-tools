from abc import ABC, abstractmethod
from ai.types import Language, Text


class Translator(ABC):
    @abstractmethod
    def Translate(self, original_text: Text, target_lang: Language) -> Text | None:
        """Translates text from a source language to a target language."""
        pass