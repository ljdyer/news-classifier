import os
import importlib
from file_helper import save_text_to_file, write_line_to_file, read_log
from typing import Callable

SAVE_ROOT = "E:/nijunen/"


# ====================
def scraper(subfolder_name: str, categories_and_pages: dict,
            get_article_hrefs: Callable, get_article_text: Callable):

    root_folder = os.path.join(CORPUS_ROOT, subfolder_name)

    for category, main_page in categories_and_pages.items():

        category_root = os.path.join(root_folder, f"{category}")
        log_file_path = os.path.join(category_root, "log.csv")
        if not os.path.isfile(log_file_path):
            save_text_to_file("", log_file_path)
        existing_files, existing_urls = read_log(log_file_path)
        next_file_num = max(
            [int(file_name.split('.')[0]) for file_name in existing_files],
            default=1
        )

        print(f"=== {category} ===\n")
        article_urls = get_article_hrefs(main_page, category)
        print(f"Attempting to get links for {len(article_urls)}",
              f"pages in category: {category}.\n")

        for article_url in article_urls:
            if article_url in existing_urls:
                print(f"{article_url}\tAlready in corpus!")
            else:
                success, result = get_article_text(article_url)
                if success:
                    file_name = f"{next_file_num}.txt"
                    file_path = os.path.join(category_root, file_name)
                    save_text_to_file(result, file_path)
                    next_file_num += 1
                    log = f"{file_name},{article_url}"
                    write_line_to_file(log, log_file_path)
                    print(f"{article_url}\t{file_name}")
                else:
                    print(f"{article_url}\t{result}")

        print("\n")

    print("Finished!")


# ====================
if __name__ == '__main__':

    """YOMIURI SHINBUN 2022
    last scraped: 4th February 2022"""
    # yomiuri_2022 = importlib.import_module('yomiuri_2022')
    # scraper(
    #     yomiuri_2022.subfolder_name, yomiuri_2022.categories_and_pages,
    #     yomiuri_2022.get_article_hrefs, yomiuri_2022.get_article_text
    # )

    """YOMIURI SHINBUN JAN 2002"""
    # yomiuri_2002 = importlib.import_module('yomiuri_2002')
    # scraper(
    #     yomiuri_2002.subfolder_name, yomiuri_2002.categories_and_pages_jan_2002,
    #     yomiuri_2002.get_article_hrefs, yomiuri_2002.get_article_text
    # )

    """YOMIURI SHINBUN AUG 2002"""
    yomiuri_2002 = importlib.import_module('yomiuri_2002')
    scraper(
        yomiuri_2002.subfolder_name,
        yomiuri_2002.categories_and_pages_aug_2002,
        yomiuri_2002.get_article_hrefs, yomiuri_2002.get_article_text
    )
