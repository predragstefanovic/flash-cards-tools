import openai
import logging
from ai.types import Language, Text
from ai.translator import Translator
from ai.editor import Editor


class _OpenAIBase:
    """A base class to handle OpenAI client initialization and requests."""
    def __init__(self, api_key: str, model: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def _make_request(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Makes a request to the OpenAI API with error handling."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature
            )
            content = response.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            logging.error(f"An unexpected error occurred during OpenAI request: {e}")
        return None # Return None on failure


class OpenAITranslator(_OpenAIBase, Translator):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key=api_key, model=model)

    def Translate(self, original_text: Text, target_lang: Language) -> Text | None:
        system_prompt = (
            f"You are a highly accurate translation engine. "
            f"Translate from {original_text.language.value} to {target_lang.value}. "
            f"Do not explain, just return the translation."
        )
        translated_contents = self._make_request(system_prompt, original_text.contents, temperature=0.2)
        if translated_contents is None:
            return None
        return Text(contents=translated_contents, language=target_lang)


class OpenAIEditor(_OpenAIBase, Editor):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key=api_key, model=model)

    def Edit(self, original_text: Text) -> Text | None:
        system_prompt = (
            f"You are a highly accurate proofreader and editor for {original_text.language.value} language. "
            f"Adjust the text to fix the typos and grammatical errors. "
            f"Do not explain, just return the corrected text. "
        )
        edited_contents = self._make_request(system_prompt, original_text.contents, temperature=0.4)
        if edited_contents is None:
            return None
        return Text(contents=edited_contents, language=original_text.language)
