from dotenv import dotenv_values
from pathlib import Path

def LoadEnvsFromDir(dirpath: str) -> dict[str, str]:
    """
    Look up all .env files in the directory, and merge their entries in a single dict
    """
    path = Path(dirpath)
    if not (path.exists() and path.is_dir()):
        raise ValueError("Dir path [" + dirpath + "] does not exist encountered while loading env files")
    
    entries = dict()
    for f in path.iterdir():
        if f.is_file() and f.name.endswith(".env"):
            d = dotenv_values(dotenv_path=f)      
            if d:
                entries = entries | d
    
    return entries