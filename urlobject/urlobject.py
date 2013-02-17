from .compat import urlparse
from .netloc import Netloc
from .path import URLPath, path_encode, path_decode
from .ports import DEFAULT_PORTS
from .query_string import QueryString
from .six import text_type, u


class URLObject(text_type):

    """
    A URL.

    This class contains properties and methods for accessing and modifying the
    constituent components of a URL. :class:`URLObject` instances are
    immutable, as they derive from the built-in ``unicode``, and therefore all
    methods return *new* objects; you need to consider this when using
    :class:`URLObject` in your own code.

    >>> from urlobject import URLObject
    >>> u = URLObject("http://www.google.com")
    """

    def __repr__(self):
        return u('URLObject(%r)') % (text_type(self),)

    @property
    def scheme(self):
        """
        Returns the scheme of the URL:

        >>> URLObject("http://www.google.com").scheme
        u'http'
        """
        return urlparse.urlsplit(self).scheme
    def with_scheme(self, scheme):
        """
        >>> URLObject("http://www.google.com").with_scheme("ftp")
        URLObject(u'ftp://www.google.com')
        """
        return self.__replace(scheme=scheme)

    @property
    def netloc(self):
        """
        >>> URLObject("http://www.google.com").netloc
        Netloc(u'www.google.com')
        """
        return Netloc(urlparse.urlsplit(self).netloc)
    def with_netloc(self, netloc):
        """
        >>> URLObject("http://www.google.com/a/b/c").with_netloc("www.amazon.com")
        URLObject(u'http://www.amazon.com/a/b/c')
        """
        return self.__replace(netloc=netloc)

    @property
    def username(self):
        """
        >>> URLObject("http://user@www.google.com").username
        u'user'
        """
        return self.netloc.username
    def with_username(self, username):
        """
        >>> URLObject("http://user@www.google.com").with_username("user2")
        URLObject(u'http://user2@www.google.com')
        """
        return self.with_netloc(self.netloc.with_username(username))
    def without_username(self):
        """
        >>> URLObject("http://user@www.google.com").without_username()
        URLObject(u'http://www.google.com')
        """
        return self.with_netloc(self.netloc.without_username())

    @property
    def password(self):
        """
        >>> URLObject("http://user:somepassword@www.google.com").password
        u'somepassword'
        """
        return self.netloc.password
    def with_password(self, password):
        """
        >>> URLObject("http://user:somepassword@www.google.com").with_password("passwd")
        URLObject(u'http://user:passwd@www.google.com')
        """
        return self.with_netloc(self.netloc.with_password(password))
    def without_password(self):
        """
        >>> URLObject("http://user:pwd@www.google.com").without_password()
        URLObject(u'http://user@www.google.com')
        """
        return self.with_netloc(self.netloc.without_password())

    @property
    def hostname(self):
        """
        >>> URLObject("http://www.google.com").hostname
        u'www.google.com'
        """
        return self.netloc.hostname
    def with_hostname(self, hostname):
        """
        >>> URLObject("http://www.google.com/a/b/c").with_hostname("cdn.amazon.com")
        URLObject(u'http://cdn.amazon.com/a/b/c')
        """
        return self.with_netloc(self.netloc.with_hostname(hostname))

    @property
    def port(self):
        """
        >>> URLObject("http://www.google.com:8080").port
        8080
        """
        return self.netloc.port
    def with_port(self, port):
        """
        >>> URLObject("http://www.google.com/a/b/c").with_port(8080)
        URLObject(u'http://www.google.com:8080/a/b/c')
        """
        return self.with_netloc(self.netloc.with_port(port))
    def without_port(self):
        """
        >>> URLObject("http://www.google.com:8080/a/b/c").without_port()
        URLObject(u'http://www.google.com/a/b/c')
        """
        return self.with_netloc(self.netloc.without_port())

    @property
    def auth(self):
        """
        >>> URLObject("http://user:password@www.google.com").auth
        (u'user', u'password')
        """
        return self.netloc.auth
    def with_auth(self, *auth):
        """
        >>> URLObject("http://user:password@www.google.com").with_auth("otheruser", "otherpassword")
        URLObject(u'http://otheruser:otherpassword@www.google.com')
        """
        return self.with_netloc(self.netloc.with_auth(*auth))
    def without_auth(self):
        """
        >>> URLObject("http://user:password@www.google.com/a/b/c").without_auth()
        URLObject(u'http://www.google.com/a/b/c')
        """
        return self.with_netloc(self.netloc.without_auth())

    @property
    def default_port(self):
        """
        The destination port number for this URL.

        If no port number is explicitly given in the URL, this will return the
        default port number for the scheme if one is known, or ``None``. The
        mapping of schemes to default ports is defined in
        :const:`urlobject.ports.DEFAULT_PORTS`.

        >>> URLObject("https://www.google.com").default_port
        443
        >>> URLObject("http://www.google.com").default_port
        80
        """
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        """
        >>> URLObject("http://www.google.com/a/b/c").path
        URLPath(u'/a/b/c')
        """
        return URLPath(urlparse.urlsplit(self).path)
    def with_path(self, path):
        """
        >>> URLObject("http://www.google.com/a/b/c").with_path("c/b/a")
        URLObject(u'http://www.google.com/c/b/a')
        """
        return self.__replace(path=path)

    @property
    def root(self):
        """
        >>> URLObject("http://www.google.com/a/b/c").root
        URLObject(u'http://www.google.com/')
        """
        return self.with_path('/')

    @property
    def parent(self):
        """
        >>> URLObject("http://www.google.com/a/b/c").parent
        URLObject(u'http://www.google.com/a/b/')
        """
        return self.with_path(self.path.parent)

    @property
    def is_leaf(self):
        """
        >>> bool(URLObject("http://www.google.com/a/b/c").is_leaf)
        True
        >>> bool(URLObject(u'http://www.google.com').is_leaf)
        False
        """
        return self.path.is_leaf

    def add_path_segment(self, segment):
        """
        >>> URLObject("http://www.google.com").add_path_segment("a")
        URLObject(u'http://www.google.com/a')
        """
        return self.with_path(self.path.add_segment(segment))

    def add_path(self, partial_path):
        """
        >>> URLObject("http://www.google.com").add_path("a/b/c")
        URLObject(u'http://www.google.com/a/b/c')
        """
        return self.with_path(self.path.add(partial_path))

    @property
    def query(self):
        """
        >>> URLObject("http://www.google.com").query
        QueryString(u'')
        >>> URLObject("http://www.google.com?a=b").query
        QueryString(u'a=b')
        """
        return QueryString(urlparse.urlsplit(self).query)
    def with_query(self, query):
        """
        >>> URLObject("http://www.google.com").with_query("a=b")
        URLObject(u'http://www.google.com?a=b')
        """
        return self.__replace(query=query)
    def without_query(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").without_query()
        URLObject(u'http://www.google.com')
        """
        return self.__replace(query='')

    @property
    def query_list(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_list
        [(u'a', u'b'), (u'c', u'd')]
        """
        return self.query.list

    @property
    def query_dict(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_dict
        {u'a': u'b', u'c': u'd'}
        """
        return self.query.dict

    @property
    def query_multi_dict(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_multi_dict
        {u'a': [u'b'], u'c': [u'd']}
        """
        return self.query.multi_dict

    def add_query_param(self, name, value):
        """
        >>> URLObject("http://www.google.com").add_query_param("a", "b").add_query_param("c", "d")
        URLObject(u'http://www.google.com?a=b&c=d')
        """
        return self.with_query(self.query.add_param(name, value))
    def add_query_params(self, *args, **kwargs):
        """
        >>> URLObject("http://www.google.com").add_query_params(a="b", c="d")
        URLObject(u'http://www.google.com?a=b&c=d')
        """
        return self.with_query(self.query.add_params(*args, **kwargs))

    def set_query_param(self, name, value):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").set_query_param("a", "z")
        URLObject(u'http://www.google.com?c=d&a=z')
        """
        return self.with_query(self.query.set_param(name, value))
    def set_query_params(self, *args, **kwargs):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").set_query_params(a="z", d="e")
        URLObject(u'http://www.google.com?c=d&a=z&d=e')
        """
        return self.with_query(self.query.set_params(*args, **kwargs))

    def del_query_param(self, name):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").del_query_param("c")
        URLObject(u'http://www.google.com?a=b')
        """
        return self.with_query(self.query.del_param(name))
    def del_query_params(self, params):
        """
        >>> URLObject("http://www.google.com?a=b&c=d&d=e").del_query_params(["c", "d"])
        URLObject(u'http://www.google.com?a=b')
        """
        return self.with_query(self.query.del_params(params))

    @property
    def fragment(self):
        """
        >>> URLObject("http://www.google.com/a/b/c#fragment").fragment
        u'fragment'
        """
        return path_decode(urlparse.urlsplit(self).fragment)
    def with_fragment(self, fragment):
        """
        >>> URLObject("http://www.google.com/a/b/c#fragment").with_fragment("new_fragment")
        URLObject(u'http://www.google.com/a/b/c#new_fragment')
        """
        return self.__replace(fragment=path_encode(fragment))
    def without_fragment(self):
        """
        >>> URLObject("http://www.google.com/a/b/c#fragment").without_fragment()
        URLObject(u'http://www.google.com/a/b/c')
        """
        return self.__replace(fragment='')

    def relative(self, other):
        """
        Resolve another URL relative to this one.

        >>> URLObject("http://www.google.com/a/b/c/").relative("../d/e/f")
        URLObject(u'http://www.google.com/a/b/d/e/f')
        """
        # Relative URL resolution involves cascading through the properties
        # from left to right, replacing
        other = type(self)(other)
        if other.scheme:
            return other
        elif other.netloc:
            return other.with_scheme(self.scheme)
        elif other.path:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path.relative(other.path))
        elif other.query:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path)
        elif other.fragment:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path).with_query(self.query)
        # Empty string just removes fragment; it's treated as a path meaning
        # 'the current location'.
        return self.without_fragment()

    def __replace(self, **replace):
        """Replace a field in the ``urlparse.SplitResult`` for this URL."""
        return type(self)(urlparse.urlunsplit(
            urlparse.urlsplit(self)._replace(**replace)))
