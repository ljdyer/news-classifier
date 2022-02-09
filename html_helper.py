from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


# ====================
def page_exists(url: str) -> bool:

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
