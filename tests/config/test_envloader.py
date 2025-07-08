import pytest
import tempfile
from pathlib import Path
from src.config.envloader import load_envs_from_dir

def test_load_envs_from_dir_merges_files():
    """
    Tests that .env files in a directory are correctly merged.
    Values in files processed later (alphabetically) should overwrite earlier ones.
    """
    with tempfile.TemporaryDirectory() as dirpath:
        p = Path(dirpath)

        # Create first .env file
        (p / "1.env").write_text("KEY_A=value_a\nSHARED_KEY=first_value")

        # Create second .env file
        (p / "2.env").write_text("KEY_B=value_b\nSHARED_KEY=second_value")

        # Create a non-env file that should be ignored
        (p / "config.txt").write_text("ignore=me")

        got = load_envs_from_dir(dirpath=dirpath)

        expected = {
            "KEY_A": "value_a",
            "KEY_B": "value_b",
            "SHARED_KEY": "second_value",
        }
        assert got == expected

def test_dir_does_not_exist():
    with pytest.raises(ValueError) as exc:
        load_envs_from_dir(dirpath="non_existent_dir/whatever")
    assert "Dir path" in str(exc.value)


        

        