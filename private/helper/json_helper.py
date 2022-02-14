import json


# ====================
def load_settings(JSON_PATH):

    with open(JSON_PATH, 'r') as file:
        settings = json.load(file)
    return settings


# ====================
def save_settings(settings, JSON_PATH):

    with open(JSON_PATH, 'w') as file:
        json.dump(settings, file, indent=4, sort_keys=True)
