from dotenv import load_dotenv
import os
from Utilities.URLFrontier import URLFrontier

load_dotenv()
URL = os.getenv("URL")
frontier = URLFrontier(["www.google.com"])

print(frontier.visit_next())

