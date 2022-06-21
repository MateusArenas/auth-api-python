# Opening HTML file
from pathlib import Path
import os

def useFile(path_to_locale):
    dir_path = os.getcwd()
    path = Path(dir_path+path_to_locale).resolve()
    file = open(path, 'r')
    return file.read()