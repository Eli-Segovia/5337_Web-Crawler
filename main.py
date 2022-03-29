from dotenv import load_dotenv
import os
from Crawler import Crawler
from urllib.parse import urlparse

load_dotenv()
URL = os.getenv("URL")
if URL is None: URL = "http://freemanmoore.net"

print('here')
Crawler.options(filter_mode='strict', url_list=[URL])
Crawler.crawl(URL)
print('here')