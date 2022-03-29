import requests
from bs4 import BeautifulSoup
from Utilities.URLFrontier import URLFrontier
from Utilities.URLFilter import URLFilter


class Crawler:
    urlFrontier = URLFrontier()
    urlFilter = URLFilter()

    @classmethod
    def options(cls, filter_mode: str, url_list: list[str]):
        cls.urlFilter.configure_urls(url_list=url_list, mode=filter_mode)

    @classmethod
    def crawl(cls, url):
        if(cls.urlFilter.allows(url)):
            cls.urlFrontier.add(url)
        cls._crawl_next()

    @classmethod
    def _crawl_next(cls):
        print("what's up")
        url = cls.urlFrontier.visit_next()
        if url is not None:
            r = requests.get(url)
            text = r.text
            print(f'Text is: {text}')
