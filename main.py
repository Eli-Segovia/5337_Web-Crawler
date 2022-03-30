from email.mime import base
from dotenv import load_dotenv
import os

from Crawler import Crawler
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

load_dotenv()
URL = os.getenv("URL")
if URL is None:
    URL = "http://freemanmoore.net"

Crawler.options(filter_mode='strict', url_list=[URL], N_Pages=100)
Crawler.crawl(URL)

# print(urlparse("mailto:fmoore@lyle.smu.edu").scheme)
