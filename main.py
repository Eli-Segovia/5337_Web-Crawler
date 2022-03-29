from dotenv import load_dotenv
import os
from Crawler import Crawler

load_dotenv()
URL = os.getenv("URL")

Crawler.crawl(URL)
