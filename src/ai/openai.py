from openai import OpenAI
from ai.translator import Translator
from ai.editor import Editor

class OpenAITranslator(Translator):
    def __init__(self, api_key: str, model: str = "gpt-4.1-nano"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def Translate(self, text: str, source_lang: str, target_lang: str) -> str:
        system_prompt = (
            f"You are a highly accurate translation engine. "
            f"Translate from {source_lang} to {target_lang}. "
            f"Do not explain, just return the translation."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
    
class OpenAIEditor(Editor):
    def __init__(self, api_key: str, model: str = "gpt-4.1-nano"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def Edit(self, text: str, lang: str) -> str:
        system_prompt = (
            f"You are a highly accurate proofreader and editor for {lang} language. "
            f"Adjust the text to fix the typos and grammatical errors. "
            f"Do not explain, just return the corrected text. "
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
    
