import pytest
from unittest.mock import MagicMock
from src.ai.openai import OpenAITranslator, OpenAIEditor
from src.ai.types import Text, Language

@pytest.fixture
def mock_openai_client() -> MagicMock:
    """
    Fixture to create a mock of the openAI client.
    This allows for direct injection into services for unit testing.
    """
    return MagicMock()

@pytest.fixture
def translator(mock_openai_client: MagicMock) -> OpenAITranslator:
    """Fixture to create an OpenAITranslator with a mocked client."""
    return OpenAITranslator(openai_client=mock_openai_client)

@pytest.fixture
def editor(mock_openai_client: MagicMock) -> OpenAIEditor:
    """Fixture to create an OpenAIEditor with a mocked client."""
    return OpenAIEditor(openai_client=mock_openai_client)

def create_mock_response(content: str | None):
    """Helper to create a mock OpenAI API response."""
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = content
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response


def test_translator_success(translator: OpenAITranslator, mock_openai_client: MagicMock):
    """
    Tests that the translator successfully calls the OpenAI API and returns a
    translated Text object.
    """
    original_text = Text(contents="Hallo Welt", language=Language.GERMAN)
    target_lang = Language.ENGLISH
    expected_translation = "Hello World"
    mock_openai_client.chat.completions.create.return_value = create_mock_response(expected_translation)

    result = translator.translate(original_text, target_lang)

    assert result is not None
    assert result.contents == expected_translation
    assert result.language == target_lang


def test_editor_success(editor: OpenAIEditor, mock_openai_client: MagicMock):
    """
    Tests that the editor successfully calls the OpenAI API and returns an
    edited Text object.
    """
    original_text = Text(contents="Das ist ein Testt", language=Language.GERMAN)
    expected_edit = "Das ist ein Test."
    mock_openai_client.chat.completions.create.return_value = create_mock_response(expected_edit)

    result = editor.edit(original_text)

    assert result is not None
    assert result.contents == expected_edit
    assert result.language == original_text.language # Language should not change


@pytest.mark.parametrize("service_fixture", ["translator", "editor"])
def test_service_handles_api_error(service_fixture: str, request: pytest.FixtureRequest, mock_openai_client: MagicMock, caplog):
    """
    Tests that services handle an API error gracefully by returning None
    and logging the error.
    """
    from openai import APIError # Import locally for test
    service = request.getfixturevalue(service_fixture)
    original_text = Text(contents="some text", language=Language.GERMAN)
    mock_openai_client.chat.completions.create.side_effect = APIError("API is down", request=None, body=None)

    if isinstance(service, OpenAITranslator):
        result = service.translate(original_text, Language.ENGLISH)
    else:
        result = service.edit(original_text)

    assert result is None
    assert "An unexpected error occurred during OpenAI request" in caplog.text
    assert "API is down" in caplog.text

@pytest.mark.parametrize("service_fixture", ["translator", "editor"])
@pytest.mark.parametrize("empty_content", [None, "", "   "])
def test_service_returns_none_on_empty_content(service_fixture: str, empty_content: str | None, request: pytest.FixtureRequest, mock_openai_client: MagicMock):
    """
    Tests that services return None if the API response content is empty or just whitespace.
    """
    service = request.getfixturevalue(service_fixture)
    original_text = Text(contents="some text", language=Language.GERMAN)
    mock_openai_client.chat.completions.create.return_value = create_mock_response(empty_content)

    if isinstance(service, OpenAITranslator):
        result = service.translate(original_text, Language.ENGLISH)
    else:
        result = service.edit(original_text)

    assert result is None
