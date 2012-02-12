import urlparse

from ports import DEFAULT_PORTS


class URLObject(unicode):

    @property
    def scheme(self):
        """The scheme component of this URL."""
        return urlparse.urlsplit(self).scheme

    def with_scheme(self, scheme):
        """Replace this URL's scheme."""
        return self.__replace(scheme=scheme)

    @property
    def netloc(self):
        """The netloc of this URL (``user:password@host:portnum``)."""
        return urlparse.urlsplit(self).netloc

    def with_netloc(self, netloc):
        """Replace this URL's netloc."""
        return self.__replace(netloc=netloc)

    @property
    def username(self):
        """The username for this URL, or ``None`` if none is present."""
        return urlparse.urlsplit(self).username

    @property
    def password(self):
        """The password for this URL, or ``None`` if none is present."""
        return urlparse.urlsplit(self).password

    @property
    def hostname(self):
        """The hostname for this URL."""
        return urlparse.urlsplit(self).hostname

    @property
    def port(self):
        """
        The port number for this URL, or ``None`` if none is explicitly given.

        See also: :attr:`default_port`.
        """
        return urlparse.urlsplit(self).port

    @property
    def default_port(self):
        """
        The destination port number for this URL.

        If no port number is explicitly given in the URL, this will return the
        default port number for the scheme if one is known, or ``None``. The
        mapping of schemes to default ports is defined in
        :const:`urlobject.ports.DEFAULT_PORTS`.
        """
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        """The path for this URL."""
        return urlparse.urlsplit(self).path

    def with_path(self, path):
        """Replace the path for this URL."""
        return self.__replace(path=path)

    @property
    def query(self):
        """This URL's query string, excluding the '?'."""
        return urlparse.urlsplit(self).query

    def with_query(self, query):
        """Replace this URL's entire query string."""
        return self.__replace(query=query)

    def without_query(self):
        """Remove this URL's entire query string, including the '?'."""
        return self.__replace(query='')

    @property
    def fragment(self):
        """This URL's fragment, excluding the '#'."""
        return urlparse.urlsplit(self).fragment

    def with_fragment(self, fragment):
        """Replace this URL's fragment."""
        return self.__replace(fragment=fragment)

    def without_fragment(self):
        """Remove this URL's fragment, including the '#'."""
        return self.__replace(fragment='')

    def __replace(self, **replace):
        """Replace a field in the ``urlparse.SplitResult`` for this URL."""
        return type(self)(urlparse.urlunsplit(
            urlparse.urlsplit(self)._replace(**replace)))
