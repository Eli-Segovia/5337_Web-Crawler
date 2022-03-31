from datetime import datetime


class CrawlerListingData:
    def __init__(self):
        self.page_data = []
        self.indexed_words: dict[str, set[str]] = dict()
        self.outgoing_links = set()
        self.broken_links = set()
        self.non_text_links = set()
        self.seen_content = {}

    def add_page(self, id, url, title, date, size, words):
        self.page_data.append({
            "id": id,
            "url": url,
            "title": title,
            "date": date,
            "size": size,
            "words": words
        })

    def add_outgoing_link(self, url):
        self.outgoing_links.add(url)

    def add_broken_link(self, url):
        self.broken_links.add(url)

    def add_non_text_links(self, url):
        self.non_text_links.add(url)
