from tabnanny import verbose
import requests
from bs4 import BeautifulSoup
from Utilities.URLFrontier import URLFrontier
from Utilities.URLFilter import URLFilter
from Utilities.CrawlerListingData import CrawlerListingData
from Utilities.WordExtractor import WordExtractor
from urllib.parse import urlparse
import os


class Crawler:
    urlFrontier = URLFrontier()
    urlFilter = URLFilter()
    crawlerData = CrawlerListingData()
    N_Pages = 0
    verbose = False

    '''
    Sets options for the crawler
    '''
    @classmethod
    def options(cls, filter_mode: str, url_list: list[str], N_Pages: int = 0, verbose=False):
        cls.urlFilter.configure_urls(url_list=url_list, mode=filter_mode)
        cls.N_Pages = N_Pages
        cls.verbose = verbose

    '''
    Begins crawling from the provided url
    '''
    @classmethod
    def crawl(cls, url):
        if not cls.verbose:
            print("Crawling...")
        if(cls.urlFilter.allows(url)):
            cls.urlFrontier.add(url)
        cls.__crawl_next()
        if not cls.verbose:
            print("Done crawling.")

    '''
    Gets the title, links, and content of the page
    '''
    @classmethod
    def __get_content(cls, r_text):
        soup = BeautifulSoup(r_text, 'html.parser')
        title = str(soup.title.string)
        links = soup.find_all('a')
        content = soup.get_text()
        return title, links, content

    '''
    Extracts the words from the content and puts them in a dictionary
    '''
    @classmethod
    def __get_words(cls, content, doc_id):
        extractor = WordExtractor(content)
        extracted = extractor.extract(cls.crawlerData.indexed_words, doc_id)
        return extracted

    '''
    wrapper function to write data into files
    '''
    @classmethod
    def write_data(cls):
        cls.__write_stats()
        cls.__write_tf()

    '''
    writes some stats into a text file
    '''
    @classmethod
    def __write_stats(cls):

        if not os.path.isdir("data"):
            os.makedirs("data")
        stats_file = open('data/stats.txt', 'w')
        stats_file.write(f'Pages indexed: {len(cls.crawlerData.page_data)}\n')

        stats_file.write("Indexed Pages:\n")
        count = 1
        for page in cls.crawlerData.page_data:
            page_data = {"title": page["title"], "id": page["id"],
                         "url": page["url"], "date": page["date"], "size": page["size"]}
            stats_file.write(f'{count}: {page_data}\n')
            count += 1
        count = 1
        stats_file.write("\n\nOutgoing Links:\n")
        for link in cls.crawlerData.outgoing_links:
            stats_file.write(f'{count}: {link}\n')
            count += 1
        count = 1
        stats_file.write("\n\nBroken Links:\n")
        for link in cls.crawlerData.broken_links:
            stats_file.write(f'{count}: {link}\n')
            count += 1
        count = 1
        stats_file.write("\n\nNon-text Files:\n")
        for link in cls.crawlerData.non_text_links:
            stats_file.write(f'{count}: {link}\n')
            count += 1
        stats_file.write(
            f"\n\nWords Indexed: {len(cls.crawlerData.indexed_words)}")
        stats_file.close()

    '''
    writes the term frequency matrix into a csv file
    '''
    @classmethod
    def __write_tf(cls):
        if not os.path.isdir("data"):
            os.makedirs("data")
        csv = open('data/term-frequency.csv', 'w')
        csv.write('Word,')
        cells = []
        header = ''
        for document in cls.crawlerData.page_data:
            cells.append(document["id"])
            header = header + (f'DOC_{document["id"]},')
        header = header.rstrip(',')
        csv.write(f'{header}\n')
        for word in cls.crawlerData.indexed_words:
            doc_ids = cls.crawlerData.indexed_words[word]
            csv.write(f'{word},')
            idx = 0
            line = ''
            for doc_id in cells:
                if doc_id in doc_ids:
                    line = line + (
                        f'{len(cls.crawlerData.page_data[idx]["words"][word])},')
                else:
                    line = line + '0,'
                idx += 1
            line = line.rstrip(',')
            csv.write(line)
            csv.write('\n')

    '''
    Adds links to the queue/frontier if they are not restricted links
    '''
    @ classmethod
    def __add_links(cls, link_list: list, curr_url):
        for link in link_list:
            url = link.get('href')
            parsed = urlparse(url)
            if parsed.hostname is None and len(parsed.scheme) == 0:
                url = f'{curr_url}/{url}'
            parsed = urlparse(url)
            if cls.verbose:
                print("Looking at link: ", parsed.geturl())
            if(parsed.scheme == 'http' or parsed.scheme == 'https'):
                if cls.urlFilter.allows(url):
                    if cls.verbose:
                        print("Added following url to queue: ", url)
                    cls.urlFrontier.add(url)

                if not cls.urlFilter.allows(f'{parsed.scheme}://{parsed.hostname}'):
                    cls.crawlerData.add_outgoing_link(url)

    '''Recursive function that grabs the next link and processes it'''
    @ classmethod
    def __crawl_next(cls):
        if cls.N_Pages <= 0:
            return
        url = cls.urlFrontier.visit_next()
        if url is not None and cls.urlFilter.allows(url):
            if cls.verbose:
                print("Analyzing the following url: ", url)
            r = requests.get(url)
            if r.status_code >= 400:
                cls.crawlerData.add_broken_link(url)
                if cls.verbose:
                    print(f'{url} responded with error code {r.status_code}')
            else:
                page_size = len(r.content)
                if r.headers['content-type'].find('text') == -1:
                    cls.crawlerData.add_non_text_links(url)
                title, links, content = cls.__get_content(r_text=r.text)
                extracted_words = cls.__get_words(content, cls.N_Pages)
                cls.__add_links(links, url)
                content_hash = hash(content)
                if content_hash not in cls.crawlerData.seen_content:
                    cls.crawlerData.seen_content[content_hash] = [cls.N_Pages]
                    cls.crawlerData.add_page(
                        cls.N_Pages, url, title, r.headers['last-modified'], page_size, extracted_words)
                else:
                    cls.crawlerData.seen_content[content_hash].append(
                        cls.N_Pages)

        cls.N_Pages -= 1
        return cls.__crawl_next()
