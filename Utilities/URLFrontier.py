from queue import Empty, Queue
from urllib.parse import urlparse


"""
Holds the urls in the frontier and maintains some state as to which sites have
already been visited.
"""


class URLFrontier:

    def __init__(self, visited_urls=[]):
        self.visited_urls = set()
        self.visited_domains = set()
        self.frontier = Queue()
        for url in visited_urls:
            self.add(url)

    '''
    Adds a url to the queue if it has not been visited
    '''

    def add(self, url):
        domain = urlparse(url).hostname
        self.visited_domains.add(domain)
        if url not in self.visited_urls:
            self.visited_urls.add(url)
            self.frontier.put(url)

    '''
    Pops the first in queue and returns it
    '''

    def visit_next(self):
        if not (self.frontier.empty()):
            return self.frontier.get()
        return None

    def is_new_domain(self, url):
        domain = urlparse(url).hostname
        return domain not in self.visited_domains
