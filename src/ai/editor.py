from abc import ABC, abstractmethod

class Editor:
    @abstractmethod
    def Edit(self, text: str, lang: str) -> str:
        """
        Edit the text to correct typos, grammatical errors and obvious stylistic issues
        """
        pass