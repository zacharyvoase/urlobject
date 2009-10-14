# -*- coding: utf-8 -*-
# urlobject.py - A utility class for operating on URLs.

from functools import partial
import cgi
import copy
import urllib
import urlparse


__author__ = 'Zachary Voase (http://zacharyvoase.com) <zacharyvoase@me.com>'
__url__ = 'http://bitbucket.org/zacharyvoase/urlobject/'
__version__ = '0.4'


URL_COMPONENTS = ('scheme', 'host', 'path', 'query', 'fragment')

SCHEME_PORT_MAP = {
    'http': 80,
    'https': 443,
    'ftp': 21,
    'ftps': 990,
}


class URLObject(unicode):
    
    """
    A utility class for manipulating URLs.
    
    >>> url = URLObject(scheme='http', host='example.com')
    >>> print url
    http://example.com/
    >>> print url / 'some' / 'path'
    http://example.com/some/path
    >>> print url & ('key', 'value')
    http://example.com/?key=value
    >>> print url & ('key', 'value') & ('key2', 'value2')
    http://example.com/?key=value&key2=value2
    >>> print url * 'fragment'
    http://example.com/#fragment
    >>> print url / u'\N{LATIN SMALL LETTER N WITH TILDE}'
    http://example.com/%C3%B1
    >>> url
    <URLObject(u'http://example.com/') at 0x...>
    
    >>> new_url = url / 'place'
    >>> new_url
    <URLObject(u'http://example.com/place') at 0x...>
    >>> new_url &= 'key', 'value'
    >>> new_url
    <URLObject(u'http://example.com/place?key=value') at 0x...>
    >>> new_url &= 'key2', 'value2'
    >>> new_url
    <URLObject(u'http://example.com/place?key=value&key2=value2') at 0x...>
    >>> new_url |= 'key', 'newvalue'
    >>> new_url
    <URLObject(u'http://example.com/place?key2=value2&key=newvalue') at 0x...>
    
    >>> auth_url = URLObject.parse(u'http://foo:bar@example.com/')
    >>> auth_url.host
    u'foo:bar@example.com'
    >>> auth_url.user
    u'foo'
    >>> auth_url.password
    u'bar'
    >>> auth_url.host_noauth
    u'example.com'
    """
    
    def __new__(cls, host='', path='/', scheme='', query=None, fragment=''):
        if not isinstance(query, basestring):
            query = encode_query(query or {}, doseq=True)
        
        return unicode.__new__(cls,
            urlparse.urlunsplit((
                encode_component(scheme),
                host.encode('idna'),
                encode_component(path),
                query,
                encode_component(fragment)
            )))
    
    @classmethod
    def parse(cls, url):
        return cls(**dict(zip(URL_COMPONENTS, urlparse.urlsplit(url))))
    
    # Support for urlobj.scheme, urlobj.host, urlobj.path, etc.
    for i, attr in enumerate(URL_COMPONENTS):
        vars()[attr] = (
            lambda index:
                property(lambda self: decode_component(
                    urlparse.urlsplit(self)[index])))(i)
        
        vars()['with_' + attr] = (
            lambda param:
                lambda self, value: self.copy(**{param: value}))(attr)
    
    # Supports without_path(), without_query() and without_fragment().
    for i, attr in enumerate(URL_COMPONENTS[2:]):
        vars()['without_' + attr] = (
            lambda param:
                lambda self: self.copy(**{param: ''}))(attr)
    
    def components(self):
        return dict(zip(URL_COMPONENTS,
                        map(partial(getattr, self), URL_COMPONENTS)))
    
    def copy(self, **kwargs):
        components = self.components()
        components.update(kwargs)
        return type(self)(**components)
    
    ## Scheme-related methods.
    
    def secure(self):
        return self.with_scheme(self.scheme + 's')
    
    ## Host-related methods.
    
    @property
    def host(self):
        return urlparse.urlsplit(self)[1].decode('idna')
    
    @property
    def host_noauth(self):
        return urllib.splituser(self.host)[1]
    
    @property
    def user(self):
        creds = urllib.splituser(self.host)[0]
        if creds:
            return urllib.splitpasswd(creds)[0]
    
    @property
    def password(self):
        creds = urllib.splituser(self.host)[0]
        if creds:
            return urllib.splitpasswd(creds)[1]
    
    def with_host(self, host):
        return self.copy(host=host)
    
    ## Port-related properties and methods.
    
    @property
    def port(self):
        host, port = urllib.splitnport(self.host, defport=None)
        if (self.scheme in SCHEME_PORT_MAP) and (not port):
            return SCHEME_PORT_MAP[self.scheme]
        return port
    
    def with_port(self, port):
        if self.scheme in SCHEME_PORT_MAP:
            if SCHEME_PORT_MAP[self.scheme] == port:
                return self.without_port()
        
        host, _ = urllib.splitport(self.host)
        return self.with_host(host + ':' + str(port))
    
    def without_port(self):
        return self.copy(host=urllib.splitport(self.host)[0])
    
    ## Query-related methods.
    
    # Overrides the automatically-defined one.
    @property
    def query(self):
        return urlparse.urlsplit(self)[3]
    
    def query_list(self):
        return decode_query(self.query)
    
    def query_dict(self, seq=True):
        if seq:
            decoded = decode_query(self.query)
            query_dict = {}
            for key, value in decoded:
                query_dict.setdefault(key, []).append(value)
            return query_dict
        
        return dict(decode_query(self.query))
    
    def add_query_param(self, key, value):
        new_query = decode_query(self.query)
        new_query.append((key, ensure_unicode(value)))
        return self.with_query(new_query)
    
    def set_query_param(self, key, value):
        old_query = self.query_list()
        new_query = []
        
        for old_key, old_value in old_query:
            if old_key != key:
                new_query.append((old_key, old_value))
        new_query.append((key, ensure_unicode(value)))
        
        return self.with_query(new_query)
    
    ## Path-related methods.
    
    def path_list(self):
        return filter(None, self.path.split('/'))
    
    def add_path_component(self, path):
        if path.startswith('/'):
            new_path = path
        elif self.path.endswith('/'):
            new_path = self.path + path
        else:
            new_path = self.path + '/' + path
        return self.with_path(new_path)
    
    def parent(self):
        try:
            parent_path = self.path[:self.path.rindex('/')]
        except IndexError:
            parent_path = '/'
        return self.with_path(parent_path)
    
    def root(self):
        return self.with_path('/')
    
    ## Additional magic methods.
    
    def __repr__(self):
        return '<URLObject(%r) at 0x%x>' % (unicode(self), id(self))
    
    def __and__(self, query_param):
        if hasattr(query_param, 'items'):
            new = self
            for qp in query_param.items():
                new = new.add_query_param(*qp)
            return new
        else:
            return self.add_query_param(*query_param)
    
    def __or__(self, query_param):
        if hasattr(query_param, 'items'):
            new = self
            for qp in query_param.items():
                new = new.set_query_param(*qp)
            return new
        else:
            return self.set_query_param(*query_param)
    
    __div__ = add_path_component
    __floordiv__ = with_path
    __mul__ = with_fragment
    __xor__ = with_port


## Functions to help with escaping international URLs.


URL_ESCAPE_RANGES = [
    (0xA0, 0xD7FF),
    (0xE000, 0xF8FF),
    (0xF900, 0xFDCF),
    (0xFDF0, 0xFFEF),
    (0x10000, 0x1FFFD),
    (0x20000, 0x2FFFD),
    (0x30000, 0x3FFFD),
    (0x40000, 0x4FFFD),
    (0x50000, 0x5FFFD),
    (0x60000, 0x6FFFD),
    (0x70000, 0x7FFFD),
    (0x80000, 0x8FFFD),
    (0x90000, 0x9FFFD),
    (0xA0000, 0xAFFFD),
    (0xB0000, 0xBFFFD),
    (0xC0000, 0xCFFFD),
    (0xD0000, 0xDFFFD),
    (0xE1000, 0xEFFFD),
    (0xF0000, 0xFFFFD),
    (0x100000, 0x10FFFD)
]


def ensure_unicode(obj):
    if isinstance(obj, unicode):
        return obj
    elif isinstance(obj, str):
        return obj.decode('utf-8')
    return unicode(obj)


def encode_component(component):
    if isinstance(component, unicode):
        encoded_list = []
        for unichar in component:
            if any(low <= ord(unichar) <= high for low, high in URL_ESCAPE_RANGES):
                encoded_list.append(urllib.quote(unichar.encode('utf-8')))
            elif ord(unichar) < 128:
                encoded_list.append(urllib.quote(str(unichar)))
            else:
                encoded_list.append(unichar)
        return ''.join(encoded_list)
    return urllib.quote(component)


def decode_component(component):
    return urllib.unquote(str(component)).decode('utf-8')


def encode_query(params, doseq=False):
    if hasattr(params, 'items'):
        params = params.items()
    if doseq:
        params = transform_doseq(params)
    return '&'.join('='.join(map(encode_component, param)) for param in params)


def transform_doseq(items):
    new_items = []
    for key, value in items:
        if hasattr(value, '__iter__') and not isinstance(value, basestring):
            for subvalue in value:
                new_items.append((key, subvalue))
        else:
            new_items.append((key, value))
    return new_items


def decode_query(query):
    return [(key.decode('utf-8'), value.decode('utf-8'))
            for key, value in cgi.parse_qsl(str(query))]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
