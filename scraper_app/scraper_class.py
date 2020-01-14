from bs4 import BeautifulSoup #noqa
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import re


class ScraperModule(object):
    """Scraper class."""

    host_urls = {
        "openload": "https://openload.co",
        "streamango": "https://streamango.com",
        "verystream": "https://verystream.com",
        "oload": "https://oload.website",
        "mixdrop": "mixdrop.co",
        "onlystream": "https://onlystream.tv/",
        "cdn": "https://animepertutticdn.com"
    }

    def __init__(self, url, host="mixdrop"):
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
            iframe_tags = self.soup.find_all('a', href=re.compile(host))
        else:
            iframe_tags = self.soup.find_all('a')
        return [uri['href'] for uri in iframe_tags]

    def get_episodes(self):
        """Loop pages and return episodes link."""
        episodes = []
        pages = self.get_pages()
        validator = URLValidator()
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
                try:
                    validator(link)
                    episodes.append(link.strip())
                except ValidationError:
                    fixed_link = re.sub('^:?//|http?s?://', 'https://', link)
                    episodes.append(fixed_link.strip())

        return episodes
