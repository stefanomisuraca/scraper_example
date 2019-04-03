from bs4 import BeautifulSoup #noqa
import requests
import re


class ScraperModule(object):
    """Scraper class."""

    host_urls = {
        "openload": "https://openload.co",
        "streamango": "https://streamango.com"
    }

    def __init__(self, url, host="openload"):
        """Initialize the object with this method."""
        self.url = url
        self.host = host
        self.html_parser = "html.parser"
        self.lxml_parser = "lxml"
        if self.url is None:
            return
        request = requests.get(self.url)
        self.content = request.content if request.status_code < 400 else None
        if self.content:
            self.soup = BeautifulSoup(self.content, self.lxml_parser)
        else:
            return None
        page_container = self.soup.find('div', class_=re.compile(
            'entry-content clearfix')
        ).find_all('a', href=True)
        self.pages = [uri['href'] for uri in page_container]
        self.pages.insert(0, self.url)

    def get_pages(self):
        """Return pages of the site."""
        return self.pages

    def get_links(self, url, host=None):
        """Return links contained in a page."""
        request = requests.get(url)
        self.content = request.content if request.status_code < 400 else None
        if self.content:
            self.soup = BeautifulSoup(self.content, self.lxml_parser)
        else:
            return
        if host:
            a_tags = self.soup.find_all('a', href=re.compile(host))
            print(a_tags)
        else:
            a_tags = self.soup.find_all('a')
        return [uri['href'] for uri in a_tags]

    def get_episodes(self):
        """Loop pages and return episodes link."""
        episodes = []
        pages = self.get_pages()
        for page in pages:
            try:
                links = self.get_links(
                    page,
                    host=self.host_urls.get(self.host)
                )
                if links is None:
                    continue
            except ValueError as e:
                print("Error - %s" % e)
                continue
            for link in links:
                episodes.append(link)

        return episodes
