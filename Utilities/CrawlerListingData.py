from datetime import datetime


class CrawlerListingData:
    def __init__(self):
        self.page_data = []
        self.outgoing_links = []
        self.broken_links = []

    def add_page(self, url, title, date, size):
        self.page_data.append({
            "url": url,
            "title": title,
            "date": date,
            "size": size
        })

    def add_outgoing_link(self, url):
        self.outgoing_links.append(url)

    def add_broken_link(self, url):
        self.broken_links.append(url)
