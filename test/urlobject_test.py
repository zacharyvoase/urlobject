import unittest

from urlobject import URLObject


class URLObjectTest(unittest.TestCase):

    def setUp(self):
        self.url_string = u"https://github.com/zacharyvoase/urlobject?spam=eggs#foo"

    def test_urlobject_preserves_equality_with_the_original_string(self):
        assert URLObject(self.url_string) == self.url_string

    def test_urlobject_preserves_the_hash_of_the_original_string(self):
        assert hash(URLObject(self.url_string)) == hash(self.url_string)

    def test_calling_unicode_on_a_urlobject_returns_a_normal_string(self):
        url = URLObject(self.url_string)
        # Normally `type(x) is Y` is a bad idea, but it's exactly what we want.
        assert type(unicode(url)) is unicode
        assert unicode(url) == self.url_string


class URLObjectPropertyTest(unittest.TestCase):

    def setUp(self):
        self.url = URLObject(u"https://github.com/zacharyvoase/urlobject?spam=eggs#foo")

    def test_scheme_returns_scheme(self):
        assert self.url.scheme == u'https'

    def test_netloc_returns_netloc(self):
        assert self.url.netloc == u'github.com'

    def test_hostname_returns_hostname(self):
        assert self.url.hostname == u'github.com'
        url = URLObject("https://user:pass@github.com:443")
        assert url.hostname == u'github.com'

    def test_port_returns_port_or_None(self):
        assert self.url.port is None
        assert URLObject("https://github.com:412").port == 412

    def test_default_port_returns_default_port_when_none_specified(self):
        assert self.url.default_port == 443

    def test_default_port_returns_given_port_when_one_is_specified(self):
        assert URLObject("https://github.com:412").default_port == 412

    def test_path_returns_path(self):
        assert self.url.path == u'/zacharyvoase/urlobject'

    def test_query_returns_query(self):
        assert self.url.query == u'spam=eggs'

    def test_fragment_returns_fragment(self):
        assert self.url.fragment == u'foo'

    def test_auth_properties_can_parse_username_and_password(self):
        url = URLObject(u'https://zack:12345@github.com/')
        assert url.username == u'zack'
        assert url.password == u'12345'

    def test_auth_properties_can_parse_username(self):
        url = URLObject(u'https://zack@github.com/')
        assert url.username == u'zack'
        assert url.password is None

    def test_auth_properties_return_None_with_no_username_or_password(self):
        url = URLObject(u'https://github.com/')
        assert url.username is None
        assert url.password is None
