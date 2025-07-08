import pytest
from unittest.mock import MagicMock

from main import process_line
from ai.types import Text, Language
from ai.editor import Editor
from ai.translator import Translator

@pytest.fixture
def mock_editor() -> MagicMock:
    return MagicMock(spec=Editor)

@pytest.fixture
def mock_translator() -> MagicMock:
    return MagicMock(spec=Translator)

def test_process_line_success(mock_editor: MagicMock, mock_translator: MagicMock):
    """Tests the happy path for processing a single line."""
    original_line = "Das ist ein Testt"
    edited_text = Text("Das ist ein Test.", Language.GERMAN)
    english_text = Text("This is a test.", Language.ENGLISH)
    serbian_text = Text("Ovo je test.", Language.SERBIAN)

    mock_editor.edit.return_value = edited_text
    # Configure the mock to return different values on subsequent calls
    mock_translator.translate.side_effect = [english_text, serbian_text]

    result = process_line(original_line, mock_editor, mock_translator)

    assert result is not None
    assert result["edited"]["contents"] == "Das ist ein Test."
    assert result["translations"][0]["contents"] == "This is a test."
    assert result["translations"][1]["contents"] == "Ovo je test."

@pytest.mark.parametrize("failed_service, log_message", [
    ("editor", "Skipping line due to editing error"),
    ("translator", "Skipping line due to English translation error"),
])
def test_process_line_handles_service_failure(
    failed_service: str, log_message: str, mock_editor: MagicMock, mock_translator: MagicMock, caplog
):
    """Tests that processing is aborted if a service fails."""
    if failed_service == "editor":
        mock_editor.edit.return_value = None
    else:
        mock_editor.edit.return_value = Text("Edited", Language.GERMAN)
        mock_translator.translate.return_value = None

    result = process_line("some line", mock_editor, mock_translator)

    assert result is None
    assert log_message in caplog.text

