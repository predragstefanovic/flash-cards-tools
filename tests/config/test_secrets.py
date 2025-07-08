import pytest
from src.config.secrets import Secrets, SecretKey

TEST_KEY = SecretKey.OPENAI_API_KEY
TEST_VALUE = "abc"

@pytest.fixture
def dummy_secrets() -> Secrets:
    """A pytest fixture for a Secrets instance with a predefined key-value pair."""
    return Secrets(entries={TEST_KEY.value: TEST_VALUE})

def test_get_secret(dummy_secrets: Secrets):
    """Tests that a secret can be retrieved successfully."""
    got = dummy_secrets.get(TEST_KEY)
    
    assert got == TEST_VALUE

def test_missing_secret():
    """Tests that a ValueError is raised for a missing secret."""
    secrets = Secrets(entries={})
    with pytest.raises(ValueError) as exc:
        secrets.get(TEST_KEY)
    assert "Value is not defined" in str(exc.value)
    
    
