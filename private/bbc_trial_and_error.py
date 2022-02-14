"""
bbc_trial_and_error.py

Module for scraping BBC news articles in desired categories from the BBC
News website by iterating through possible article ids and checking whether
an article in any of the desired categories exists at the corresponding URL.

This method has the advantage that it can be left to run in the background
and could potentially pick up a very large number of articles, however in
practice it has been found to be very slow as due to the large number of
categories the hit rate is very low. The method in bbc_from_category_pages.py
is preferred but this module is left as a backup method to pick up a few extra
articles every now and then if desired.

How to use:
1. Just run the program in the terminal as follows (no parameters required).
   > python bbc_trial_and_error.py
2. You can exit the program gracefully at any time by pressing Ctrl + C.
   The program will print a mesage to let you know which id it had checked up
   to and will update ids_to_check.json so that it can start off where it left
   off in the next execution.
3. Settings can be changed in the settings file specified in CONFIG_JSON

The process is as follows:
1. Iterate through ids in range.
2. Create the url that an article belonging to each category with the relevant
   id would have if such an article exists.
3. If an article exists at the URL, get the text from it.
4. If a file with the same name does not already exist, create it and inform
   the user that a new article was added by adding one to the counter for
   that category.
"""

import os
from os.path import isfile

from helper.json_helper import load_settings, save_settings
from helper.file_helper import save_text_to_file
from helper.html_helper import get_bbc_article_text

CONFIG_JSON = 'config.json'


# ====================
def make_url(url_root: str, category: str, id: int) -> str:
    """Return a (possible) URL for an article with the category
    and id specified."""

    return f"{url_root}{category}-{id}"


# ====================
def make_file_path(save_root: str, category: str, id: int) -> str:
    """Return the path to which to save article text"""

    return f"{save_root}{category}-{id}.txt"


# ====================
def update_display(articles_added_counter: dict):
    """Update the display with the counters of articles added for each
    category."""

    os.system('cls')

    for category, count in articles_added_counter.items():
        print(f'{category}: {count}')


# ====================
def main():

    SETTINGS = load_settings(CONFIG_JSON)
    CATEGORIES = SETTINGS['BBC_CATEGORIES']
    articles_added_counter = {
        category: 0
        for category in (CATEGORIES + ['ALREADY SAVED'])
    }

    try:
        for id in range(SETTINGS['IDS']['start'], SETTINGS['IDS']['end']):
            update_display(articles_added_counter)
            print(f"Processing id: {id}")
            for category in CATEGORIES:
                url = make_url(SETTINGS['URL_ROOT'], category, id)
                success, text = get_bbc_article_text(url)
                if success:
                    file_path = make_file_path(
                        SETTINGS['SAVE_ROOT'], category, id
                    )
                    if not isfile(file_path):
                        save_text_to_file(text, file_path)
                        articles_added_counter[category] += 1
                    else:
                        articles_added_counter['ALREADY SAVED'] += 1

    except KeyboardInterrupt:
        print("You terminated the program while it was checking",
              f"ID: {id}")

    except Exception as e:
        print(f"The program terminated due to a <<<{e}>>> error",
              f"while it was checking ID: {id}")

    else:
        print("Finished checking all IDs!")

    finally:
        SETTINGS['IDS']['start'] = id
        save_settings(SETTINGS, CONFIG_JSON)
        print(f"Settings saved to {CONFIG_JSON}.")


# ====================
if __name__ == "__main__":

    main()
