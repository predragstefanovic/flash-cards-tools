from abc import ABC, abstractmethod

class Translator:
    @abstractmethod
    def Translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source_lang to target_lang using an AI client.
        """
        pass