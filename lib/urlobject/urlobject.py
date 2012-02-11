import urlparse

from ports import DEFAULT_PORTS


class URLObject(unicode):

    @property
    def scheme(self):
        """Return the scheme component of this URL."""
        return urlparse.urlsplit(self).scheme

    @property
    def netloc(self):
        """Return the netloc of this URL (``user:password@host:portnum``)."""
        return urlparse.urlsplit(self).netloc

    @property
    def username(self):
        return urlparse.urlsplit(self).username

    @property
    def password(self):
        return urlparse.urlsplit(self).password

    @property
    def hostname(self):
        return urlparse.urlsplit(self).hostname

    @property
    def port(self):
        return urlparse.urlsplit(self).port

    @property
    def default_port(self):
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        return urlparse.urlsplit(self)[2]

    @property
    def query(self):
        return urlparse.urlsplit(self)[3]

    @property
    def fragment(self):
        return urlparse.urlsplit(self)[4]
