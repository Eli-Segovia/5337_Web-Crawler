from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

'''
Maintains state as to which URLs are allowed or restricted

if in "strict" mode, then we can only visit the allowed domains barring any url
that is in the restricted set.

if in "open" mode, then we can visit any url EXCEPT for what is provided in 
the restricted set. the allowed set is ignored.
'''


def add_url_to_set(url_list: list[str], target_set: set[str], domain_only=False):
    for url in url_list:
        if domain_only:
            url = urlparse(url).hostname
            if url is None:
                continue
        target_set.add(url)


class URLFilter:

    def __init__(self):
        self.restricted = set()
        self.allowed = set()
        self.mode = None

    '''
    Configures the urls that are restricted/allowed
    '''

    def configure_urls(self, url_list: list[str], mode: str):
        if mode == 'open':
            # allowed should be cleared. not needed.
            if len(self.allowed) != 0:
                self.allowed.clear()

            # throw any provided url into restricted set
            add_url_to_set(url_list, self.restricted)

        elif mode == 'strict':
            # throw any domain into the allowed set.
            # TODO need to grab domain name only from this list...
            add_url_to_set(url_list, self.allowed, domain_only=True)

        else:
            raise ValueError("Mode must be set to be 'strict' or 'open'")
        # set member mode to appropriate mode
        self.mode = mode

    def restrict_urls(self, url_list):
        add_url_to_set(url_list, self.restricted)

    def allows(self, url):
        parsed = urlparse(url)
        robot = RobotFileParser()
        robot.set_url(f'{parsed.scheme}://{parsed.hostname}/robots.txt')
        robot.read()
        robot_allowed = robot.can_fetch('*', url)
        if self.mode == 'strict':
            return parsed.hostname in self.allowed and url not in self.restricted and robot_allowed
        elif self.mode == 'open':
            return url not in self.restricted and robot_allowed
        else:
            raise ValueError("Mode must be set to be 'strict' or 'open'")
