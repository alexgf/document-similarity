class PageNotFoundException(Exception):
    """ Exception raised when URL is not found

        Attributes:
         url - url not possible to be loaded
    """

    def __init__(self, url):
        self.url = url
        self.message = f'Enable to load {self.url}'