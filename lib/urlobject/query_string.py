import urlparse


class QueryString(unicode):

    @property
    def list(self):
        return urlparse.parse_qsl(self.encode('utf-8'))
