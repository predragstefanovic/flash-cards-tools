from abc import ABC, abstractmethod
from ai.types import Text


class Editor(ABC):
    @abstractmethod
    def Edit(self, original_text: Text) -> Text | None:
        """Edits and proofreads text in a given language."""
        pass