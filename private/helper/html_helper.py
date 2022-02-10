from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


# ====================
def get_bbc_article_text(url: str) -> str:
    """Get the article text from a BBC News article url"""

    # Try to get the page HTML
    try:
        bs = get_bs(url)
    except Exception as e:
        return (False, f'<<<{e}>>> error while getting HTML from {url}!')

    # Get text from all <p> tags inside <article> tag
    try:
        article = bs.findAll(name='article')
        article_children = article[0].findChildren("p")
        article_text = get_all_text(article_children)
        return (True, article_text)
    except Exception as e:
        return (False, f"<<<{e}>>> error while parsing {url}!")


# ====================
def page_exists(url: str) -> bool:
    """Return True if a page exists at the given URL"""

    try:
        status_code = request.urlopen(url).getcode()
        if status_code == 200:
            return True
    except HTTPError:
        return False


# ====================
def get_bs(url: str) -> BeautifulSoup:
    """Get BeautifulSoup object from URL"""

    with request.urlopen(url) as response:
        html = response.read()
    bs = BeautifulSoup(html, 'html.parser')
    return bs


# ====================
def get_html(url: str) -> str:
    """Get HTML from URL"""

    html = request.urlopen(url).read()
    return html


# ====================
def bs_from_html(html: str) -> BeautifulSoup:
    """Get BeautifulSoup object from HTML"""

    bs = BeautifulSoup(html, 'html.parser')
    return bs


# ====================
def get_all_text(tag) -> str:
    """Get text from all tags contained in bs4 ResultSet"""

    return '\n\n'.join([t.text.strip() for t in tag])


# ====================
def get_all_link_urls(url: str) -> list:

    bs = get_bs(url)
    return [a['href'] for a in bs.find_all('a', href=True)]
