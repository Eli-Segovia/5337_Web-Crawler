from queue import Queue
class URLFrontier:

    def __init__(self, visited_urls):
        self.visited_urls = set()
        self.frontier = Queue()
        for url in visited_urls:
            self.add(url)
    
    def add(self, url):
        if url not in self.visited_urls:
            self.visited_urls.add(url)
            self.frontier.put(url)

    def visit_next(self):
        return self.frontier.get()