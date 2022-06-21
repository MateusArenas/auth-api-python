# Opening JSON file
from pathlib import Path
import os
import json

def useJSON(path_to_locale):
    dir_path = os.getcwd()
    path = Path(dir_path+path_to_locale).resolve()
    loader = open(path)
    return json.load(loader)