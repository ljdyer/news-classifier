"""
bbc_from_category_pages.py

Module for scraping BBC news articles in desired categories from the BBC
News website by getting article names from links on category pages.

How to use:
1. Just run the program in the terminal as follows (no parameters required).
   > python bbc_from_category_pages.py
2. You can exit the program gracefully at any time by pressing Ctrl + C.
   The program will exit with a message to let you know which category page
   it was scraping.
3. Changes to CATEGORIES and CATEGORY_PAGES can be applied directly in the
   program.

The process is as follows:
1. For each category url specified in CATEGORY_PAGES, get all link targets
   from the page.
2. For each link, check whether it satisfies the conditions for being an
   article belonging to one of the categories in CATEGORIES.
3. If a file with the same name does not already exist, create it and inform
   the user that a new article was added by adding one to the counter for
   that category.
"""

from helper.html_helper import (
    get_all_link_urls, get_bbc_article_text
)
from helper.file_helper import save_text_to_file
import os
from os.path import isfile

URL_ROOT = "https://www.bbc.co.uk/news/"
SAVE_ROOT = "articles/"
CATEGORIES = [
    'health',
    'science-environment',
    'business',
    'technology',
    'entertainment-arts'
]
CATEGORY_PAGES = [
    'https://www.bbc.co.uk/news/coronavirus',
    'https://www.bbc.co.uk/news/science-environment-56837908',
    'https://www.bbc.co.uk/news/business',
    'https://www.bbc.co.uk/news/technology',
    'https://www.bbc.co.uk/news/science_and_environment',
    'https://www.bbc.co.uk/news/health',
    'https://www.bbc.co.uk/news/entertainment_and_arts',
]

articles_added_counter = {
    category: 0 for category in CATEGORIES + ['ALREADY SAVED']
}


# ====================
def make_url(article_name: str) -> str:
    """Return a (possible) URL for an article with name article_name
    by prepending URL_ROOT"""

    return f"{URL_ROOT}{article_name}"


# ====================
def make_file_path(article_name: str) -> str:
    """Return the path to which to save article text"""

    return f"{SAVE_ROOT}{article_name}.txt"


# ====================
def article_category(article_name: str):
    """Check whether an article belongs to any of the categories in CATEGORIES.

    If it does, return the category as a string. Otherwise, return None."""

    for category in CATEGORIES:
        # Use startswith to filter out article names like
        # uk-scotland-scotland-business-60318195
        if article_name.startswith(category):
            return category
    else:
        return None


# ====================
def update_display():
    """Update the display with the counters of articles added for each
    category."""

    os.system('cls')
    for category, count in articles_added_counter.items():
        print(f'{category}: {count}')


# ====================
def main():
    try:
        update_display()
        for page in CATEGORY_PAGES:
            link_urls = get_all_link_urls(page)
            for url in link_urls:
                article_name = url.rpartition('/')[2]
                if category := article_category(article_name):
                    url = make_url(article_name)
                    success, text = get_bbc_article_text(url)
                    if success:
                        file_path = make_file_path(article_name)
                        if not isfile(file_path):
                            save_text_to_file(text, file_path)
                            articles_added_counter[category] += 1
                        else:
                            articles_added_counter['ALREADY SAVED'] += 1
                        update_display()

    except KeyboardInterrupt:
        print(f"Program terminated while scraping page: {page}")
        quit()


# ====================
if __name__ == "__main__":

    main()
