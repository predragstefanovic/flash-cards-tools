from enum import Enum

class SecretKey(Enum):
    OPENAI_API_KEY = "OPENAI_API_KEY"

class Secrets:
    def __init__(self, entries: dict[str, str]):
        self.secrets = entries.copy()


    def get(self, key: SecretKey) -> str:
        value = self.secrets.get(key.value)
        if not value:
            raise ValueError("Value is not defined for the secret key [" + key.value + "]")
        return value
    
