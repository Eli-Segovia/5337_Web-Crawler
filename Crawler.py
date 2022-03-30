import requests
from bs4 import BeautifulSoup
from Utilities.URLFrontier import URLFrontier
from Utilities.URLFilter import URLFilter
from Utilities.CrawlerListingData import CrawlerListingData
from urllib.parse import urlparse


class Crawler:
    urlFrontier = URLFrontier()
    urlFilter = URLFilter()
    crawlerData = CrawlerListingData()
    N_Pages = 0
    is_polite = True

    @classmethod
    def options(cls, filter_mode: str, url_list: list[str], N_Pages: int = 0):
        cls.urlFilter.configure_urls(url_list=url_list, mode=filter_mode)
        cls.N_Pages = N_Pages

    @classmethod
    def crawl(cls, url):
        if(cls.urlFilter.allows(url)):
            cls.urlFrontier.add(url)
        cls.__crawl_next()

    @classmethod
    def __get_content(cls, r_text):
        soup = BeautifulSoup(r_text, 'html.parser')
        # print(r_text)
        title = str(soup.title.string)
        links = soup.find_all('a')
        return title, links

    @classmethod
    def __add_links(cls, link_list: list, curr_url):
        for link in link_list:
            url = link.get('href')
            parsed = urlparse(url)
            if parsed.hostname is None and len(parsed.scheme) == 0:
                url = f'{curr_url}/{url}'
            parsed = urlparse(url)
            print("Looking at link: ", parsed.geturl())
            if(parsed.scheme == 'http' or parsed.scheme == 'https'):
                if cls.urlFilter.allows(url):
                    print("added", url)
                    cls.urlFrontier.add(url)

                if not cls.urlFilter.allows(f'{parsed.scheme}://{parsed.hostname}'):
                    cls.crawlerData.add_outgoing_link(url)

    @ classmethod
    def __crawl_next(cls):
        print(cls.N_Pages)
        if cls.N_Pages <= 0:
            return
        url = cls.urlFrontier.visit_next()
        cls.N_Pages -= 1
        if url is not None and cls.urlFilter.allows(url):
            print("Currently at ", url)
            r = requests.get(url)
            if r.status_code >= 400:
                cls.crawlerData.add_broken_link(url)
                print(f'{url} responded with error code {r.status_code}')
            else:
                page_size = len(r.content)
                title, links = cls.__get_content(r_text=r.text)
                cls.__add_links(links, url)
                cls.crawlerData.add_page(url, title, "N/A", page_size)
        return cls.__crawl_next()
