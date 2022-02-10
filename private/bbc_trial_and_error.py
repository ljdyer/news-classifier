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
   to and will update ids_to_check.txt so that it can start off where it left off
   in the next execution.
3. Changes to CATEGORIES can be applied directly in the program.

The process is as follows:
1. Iterate through ids in range.
2. Create the url that an article belonging to each category with the relevant id
   would have such an article exists.
3. If an article exists at the URL, get the text from it.
4. If a file with the same name does not already exist, create it and inform
   the user that a new article was added by adding one to the counter for
   that category.
"""

from helper.html_helper import page_exists, get_bs, get_bbc_article_text
from helper.file_helper import save_text_to_file
import os

URL_ROOT = "https://www.bbc.co.uk/news/"
SAVE_ROOT = "articles/"
CATEGORIES = [
    'health',
    'science-environment',
    'business',
    'technology',
    'entertainment-arts'
]

# ====================
def make_url(category: str, id: int) -> str:
    """Return a (possible) URL for an article with the category
    and id specified."""
    
    return f"{URL_ROOT}{category}-{id}"


# ====================
def make_file_path(category: str, id: int) -> str:
    """Return the path to which to save article text"""

    return f"{SAVE_ROOT}{category}-{id}.txt"


articles_added_counter = {category: 0 for category in CATEGORIES}

IDS = range(60044994, 60290065)


# ====================
def main():
    try:
        for id in IDS:
            os.system('cls')
            print(f"Processing id: {id}")
            for category, count in articles_added_counter.items():
            
                if page_exists(url):
                    success, text = get_bbc_article_text(url)
                    if success:
                        file_path = make_file_path(category, id)
                        save_text_to_file(text, file_path)
                        articles_added_counter[category] += 1
    exc


# ====================
if __name__ == "__main__":

    main()
