from dotenv import load_dotenv
import os
import sys

from Crawler import Crawler

load_dotenv()
URL = os.getenv("URL")
if URL is None:
    URL = "http://freemanmoore.net"
if len(sys.argv) < 2:
    N_PAGES = 100
else:
    N_PAGES = int(sys.argv[1])

Crawler.options(filter_mode='strict', url_list=[
                URL], N_Pages=N_PAGES, verbose=False)
Crawler.crawl(URL)
Crawler.write_data()
