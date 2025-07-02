from ai.translator import Translator
from ai.editor import Editor
from ai.openai import OpenAITranslator
from ai.openai import OpenAIEditor
from config.secrets import Secrets, SecretKey
from config.envloader import LoadEnvsFromDir

secrets_dirpath = "configs/secrets"

def Init() -> tuple[Translator, Editor]:
    secrets = Secrets(entries=LoadEnvsFromDir(dirpath=secrets_dirpath))
    translator = OpenAITranslator(api_key=secrets.Get(SecretKey.OPENAI_API_KEY))
    editor = OpenAIEditor(api_key=secrets.Get(SecretKey.OPENAI_API_KEY))

    return (translator, editor)

    