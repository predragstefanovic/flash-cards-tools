import pytest
import tempfile
from src.config.envloader import load_envs_from_dir

def test_read_env_file(): 
    basepath = "test/resources"
    key = "SOME_KEY"
    value = 10
    with tempfile.TemporaryDirectory(dir=basepath) as dirpath:
        for x in range(0, value+1):
            filepath = dirpath + "/" + ".test_env_file.env"
            fp = open(filepath, "w")
            fp.write(key + "=" + str(x) + "\n")
            fp.flush()
            fp.close()
            
        got = load_envs_from_dir(dirpath=dirpath)
        assert key in got.keys()
        assert str(value) == got[key]


def test_dir_does_not_exist():
    with pytest.raises(ValueError) as exc:
        load_envs_from_dir(dirpath="whatever")
    assert "Dir path" in str(exc.value)


        

        