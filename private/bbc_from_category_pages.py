from helper.html_helper import get_bs, get_all_text, get_all_link_urls, page_exists
from helper.file_helper import save_text_to_file
import os

URL_ROOT = "https://www.bbc.co.uk/news/"
make_url = lambda article_name : f"{URL_ROOT}{article_name}"

SAVE_ROOT = "articles/"
make_file_path = lambda article_name : f"{SAVE_ROOT}{article_name}.txt"

CATEGORIES = [
    'health',
    'science-environment',
    'business',
    'technology',
    'entertainment-arts'
]

ARTICLE_PAGES = [
    'https://www.bbc.co.uk/news/coronavirus',
    'https://www.bbc.co.uk/news/science-environment-56837908',
    'https://www.bbc.co.uk/news/business',
    'https://www.bbc.co.uk/news/technology',
    'https://www.bbc.co.uk/news/science_and_environment',
    'https://www.bbc.co.uk/news/health',
    'https://www.bbc.co.uk/news/entertainment_and_arts',
]

category_counts = {category: 0 for category in CATEGORIES}


# ====================
def update_display(category_counts: dict):

    os.system('cls')
    for category, count in category_counts.items():
        print(f'{category}: {count}')


# ====================
def main():
    try:
        update_display(category_counts)
        for page in ARTICLE_PAGES:
            link_urls = get_all_link_urls(page)
            for url in link_urls:
                article_name = url.rpartition('/')[2]
                for category in CATEGORIES:
                    if category in article_name:
                        url = make_url(article_name)
                        if page_exists(url):
                            success, text = get_article_text(url)
                            if success:
                                file_path = make_file_path(article_name)
                                save_text_to_file(text, file_path)
                                category_counts[category] += 1
                                update_display(category_counts)

    except KeyboardInterrupt:
        print(f"Program terminated while scraping page: {page}")
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