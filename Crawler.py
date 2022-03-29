import requests
from bs4 import BeautifulSoup
from Utilities.URLFrontier import URLFrontier


class Crawler:
    urlFrontier = URLFrontier()

    @classmethod
    def crawl(cls, url):
        cls.urlFrontier.add(url)
        cls._crawl_next()

    @classmethod
    def _crawl_next(cls):
        url = cls.urlFrontier.visit_next()
        if url is not None:
            r = requests.get(url)
            text = r.text
            print(f'Text is: {text}')
