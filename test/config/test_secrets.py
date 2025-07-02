import pytest
from src.config.secrets import Secrets, SecretKey

test_key = SecretKey.OPENAI_API_KEY
test_value = "abc"
def setup_dummy_secrets() -> Secrets:
    d = dict()
    d[test_key.value] = test_value
    return Secrets(entries=d)


def test_get_secret():
    secrets = setup_dummy_secrets()
    got = secrets.Get(test_key)
    
    assert got == test_value 

def test_missing_secret():
    secrets = Secrets(dict())
    with pytest.raises(ValueError) as exc:
        secrets.Get(test_key)
    assert "Value is not defined" in str(exc.value)
    
    
