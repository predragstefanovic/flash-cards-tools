from openai import OpenAI
from src.ai.translator import Translator
from src.ai.editor import Editor
from src.ai.openai import OpenAITranslator
from src.ai.openai import OpenAIEditor
from src.config.secrets import Secrets, SecretKey
from src.config.envloader import load_envs_from_dir

SECRETS_DIRPATH = "configs/secrets"

def initialize_services() -> tuple[Translator, Editor]:
    secrets = Secrets(entries=load_envs_from_dir(dirpath=SECRETS_DIRPATH))
    api_key = secrets.get(SecretKey.OPENAI_API_KEY)
    openai_client = OpenAI(api_key=api_key)
    translator = OpenAITranslator(openai_client)
    editor = OpenAIEditor(openai_client)

    return (translator, editor)

    