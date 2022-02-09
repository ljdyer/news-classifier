from helper.html_helper import page_exists, get_bs, get_all_text
from helper.file_helper import save_text_to_file
import os

URL_ROOT = "https://www.bbc.co.uk/news/"
make_url = lambda category, id : f"{URL_ROOT}{category}-{id}"

SAVE_ROOT = "articles/"
make_file_path = lambda category, id : f"{SAVE_ROOT}{category}-{id}.txt"

CATEGORIES = [
    'health',
    'science-environment',
    'business',
    'technology',
    'entertainment-arts'
]

CATEGORY_COUNTS = {category: 0 for category in CATEGORIES}

IDS = range(60044994, 60290065)


# ====================
def main():
    try:
        for id in IDS:
            os.system('cls')
            print(f"Processing id: {id}")
            for category, count in CATEGORY_COUNTS.items():
                print(f'{category}: {count}')
            for category in CATEGORIES:
                url = make_url(category, id)
                if page_exists(url):
                    success, text = get_article_text(url)
                    if success:
                        file_path = make_file_path(category, id)
                        save_text_to_file(text, file_path)
                        CATEGORY_COUNTS[category] += 1
    except KeyboardInterrupt:
        print(f"Program terminated while processing id: {id}")
        quit()


# ====================
def get_article_text(url: str) -> str:

    # Try to get the page HTML
    try:
        bs = get_bs(url)
    except Exception as e:
        return (False, f'{e} error while getting HTML!')

    # Get text from all <p> tags inside <article> tag
    try:
        article = bs.findAll(name='article')
        article_children = article[0].findChildren("p")
        article_text = get_all_text(article_children)
        return (True, article_text)
    except Exception as e:
        return (False, f"{e} error while parsing!")


# ====================
if __name__ == "__main__":

    main()