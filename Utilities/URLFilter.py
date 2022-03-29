from urllib.parse import urlparse

'''
Maintains state as to which URLs are allowed or restricted

if in "strict" mode, then we can only visit the allowed domains barring any url
that is in the restricted set.

if in "open" mode, then we can visit any url EXCEPT for what is provided in 
the restricted set. the allowed set is ignored.
'''

def add_url_to_set(url_list: list[str], target_set: set[str]):
    for url in url_list:
        target_set.add(url)

class URLFilter:

    def __init__(self):
        self.restricted = set()
        self.allowed = set()
        self.mode = None

    def configure_urls(self, url_list, mode):
        if mode == 'open':
            # allowed should be cleared. not needed.
            if len(self.allowed) != 0:
                self.allowed.clear()
            # throw any provided url into restricted set
            self.restrict_urls(url_list)

        elif mode == 'strict':
            # throw any domain into the allowed set.
           add_url_to_set(url_list, self.allowed)

        else:
            raise ValueError("Mode can only be 'restrict' or 'allow'")
        # set member mode to appropriate mode
        self.mode = mode

    def restrict_urls(self, url_list):
        add_url_to_set(url_list, self.restricted)
    
    def is_allowed(self, url):
        if self.mode == 'allow':
            return url in self.allowed
        elif self.mode == 'restrict':
            return url not in self.restricted
        else:
            raise ValueError("Mode can only be 'restrict' or 'allow'")
