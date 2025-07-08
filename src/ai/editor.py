from abc import ABC, abstractmethod
from src.ai.types import Text


class Editor(ABC):
    @abstractmethod
    def edit(self, original_text: Text) -> Text | None:
        """Edits and proofreads text in a given language."""
        pass