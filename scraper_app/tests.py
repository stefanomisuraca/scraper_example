from django.test import TestCase
from scraper_app.scraper_class import ScraperModule


class TestLinks(TestCase):
    """Test for scraper module."""

    def setUp(self):
        """Set up test data."""
        self.anime_link = "https://animepertutti.com/sword-art-online-alicization-war-of-underworld-sub-ita-streaming-download-z" #noqa

    def test_scraper(self):
        """Test scraper module success."""
        scrap = ScraperModule(url=self.anime_link, host="mixdrop")
        pages = scrap.pages
        print(f"pages: {pages}")
        get_pages = scrap.get_pages()
        first_link = scrap.get_links(pages[0])
        print(first_link)
        episodes = scrap.get_episodes()
        print(episodes)
