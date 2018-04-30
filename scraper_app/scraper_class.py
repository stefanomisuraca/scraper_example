from bs4 import BeautifulSoup
import requests
import re


class ScraperModule(object):

    def __init__(self, url):
        self.url = url
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
        page_container = self.soup.find('div', class_=re.compile('pagination clearfix')).find_all('a', href=True)
        self.pages = [uri['href'] for uri in page_container]
        self.pages.insert(0, self.url)

    def get_pages(self):
        return self.pages

    def get_links(self, url, host=None):
        request = requests.get(url)
        self.content = request.content if request.status_code < 400 else None
        if self.content:
            self.soup = BeautifulSoup(self.content, self.lxml_parser)
        else:
            return
        if host:
            a_tags = self.soup.find_all('a', href=re.compile(host))
        else:
            a_tags = self.soup.find_all('a')
        return [uri['href'] for uri in a_tags]

    def get_episodes(self):
        episodes = []
        pages = self.get_pages()
        for page in pages:
            links = self.get_links(page, host="https://openload.co")
            for link in links:
                episodes.append(link)

        return episodes
