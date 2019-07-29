from bs4 import BeautifulSoup #noqa
import requests
import re


class ScraperModule(object):
    """Scraper class."""

    host_urls = {
        "openload": "https://openload.co",
        "streamango": "https://streamango.com",
        "verystream": "https://verystream.com",
        "oload": "https://oload.website"
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
        self.pages = [uri["href"] for uri in self.soup.find_all(
            'a', class_="post-page-numbers"
        )]
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
            iframe_tags = self.soup.find_all('iframe', src=re.compile(host))
            print(iframe_tags)
        else:
            iframe_tags = self.soup.find_all('iframe')
        return [uri['src'] for uri in iframe_tags]

    def get_episodes(self):
        """Loop pages and return episodes link."""
        episodes = []
        pages = self.get_pages()
        for page in pages:
            print(page)
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
