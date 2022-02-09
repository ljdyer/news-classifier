import os
from os import listdir
from os.path import isfile, join


# ====================
def save_text_to_file(text: str, file_path: str):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)


# ====================
def get_text_from_file(file_path: str) -> str:

    with open(file_path) as f:
        text = f.read()
    return text


# ====================
def get_file_names(folder_path: str) -> list:

    return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]