from dotenv import load_dotenv
import os
from Crawler import Crawler
from urllib.parse import urlparse

load_dotenv()
URL = os.getenv("URL")

# Crawler.crawl(URL)
