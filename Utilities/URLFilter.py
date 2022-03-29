class URLFilter:

    def __init__(self):
        self.restricted = set()
        self.allowed = set()

    def configure_urls(self, url_list, mode):
        if mode == 'restrict':
            if len(self.allowed) != 0:
                self.allowed.clear()
            for url in url_list:
                self.restricted.add(url)

        elif mode == 'allow':
            if len(self.restricted) != 0:
                self.restricted.clear()
            for url in url_list:
                self.allowed.add(url)

        else:
            raise ValueError("Mode can only be 'restrict' or 'allow'")
