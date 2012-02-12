import unittest

from nose.tools import assert_raises

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


class URLObjectModificationTest(unittest.TestCase):

    def setUp(self):
        self.url = URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_scheme_replaces_scheme(self):
        assert (self.url.with_scheme('http') ==
                u'http://github.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_netloc_replaces_netloc(self):
        assert (self.url.with_netloc('example.com') ==
                u'https://example.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_username_adds_username(self):
        url = URLObject(u'https://github.com/')
        assert url.with_username('zack') == u'https://zack@github.com/'

    def test_with_username_replaces_username(self):
        url = URLObject(u'https://zack@github.com/')
        assert url.with_username('alice') == u'https://alice@github.com/'

    def test_without_username_removes_username(self):
        url = URLObject(u'https://zack@github.com/')
        assert url.without_username() == u'https://github.com/'

    def test_with_password_adds_password(self):
        url = URLObject(u'https://zack@github.com/')
        assert url.with_password('1234') == u'https://zack:1234@github.com/'

    def test_with_password_raises_ValueError_when_there_is_no_username(self):
        url = URLObject(u'https://github.com/')
        assert_raises(ValueError, lambda: url.with_password('1234'))

    def test_with_password_replaces_password(self):
        url = URLObject(u'https://zack:1234@github.com/')
        assert url.with_password('5678') == u'https://zack:5678@github.com/'

    def test_without_password_removes_password(self):
        url = URLObject(u'https://zack:1234@github.com/')
        assert url.without_password() == u'https://zack@github.com/'

    def test_with_auth_with_one_arg_adds_username(self):
        url = URLObject(u'https://github.com/')
        assert url.with_auth('zack') == u'https://zack@github.com/'

    def test_with_auth_with_one_arg_replaces_whole_auth_string_with_username(self):
        url = URLObject(u'https://alice:1234@github.com/')
        assert url.with_auth('zack') == u'https://zack@github.com/'

    def test_with_auth_with_two_args_adds_username_and_password(self):
        url = URLObject(u'https://github.com/')
        assert url.with_auth('zack', '1234') == u'https://zack:1234@github.com/'

    def test_with_auth_with_two_args_replaces_whole_auth_string_with_username_and_password(self):
        # Replaces username-only auth string
        url = URLObject(u'https://alice@github.com/')
        assert url.with_auth('zack', '1234') == u'https://zack:1234@github.com/'

        # Replaces username and password.
        url = URLObject(u'https://alice:4567@github.com/')
        assert url.with_auth('zack', '1234') == u'https://zack:1234@github.com/'

    def test_without_auth_removes_entire_auth_string(self):
        # No username or password => no-op.
        url = URLObject(u'https://github.com/')
        assert url.without_auth() == u'https://github.com/'
        # Username-only.
        url = URLObject(u'https://alice@github.com/')
        assert url.without_auth() == u'https://github.com/'
        # Username and password.
        url = URLObject(u'https://alice:1234@github.com/')
        assert url.without_auth() == u'https://github.com/'

    def test_with_port_adds_port_number(self):
        assert (self.url.with_port(24) ==
                u'https://github.com:24/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_port_replaces_port_number(self):
        url = URLObject(u'https://github.com:59/')
        assert url.with_port(67) == u'https://github.com:67/'

    def test_without_port_removes_port_number(self):
        url = URLObject(u'https://github.com:59/')
        assert url.without_port() == u'https://github.com/'

    def test_with_path_replaces_path(self):
        assert (self.url.with_path('/dvxhouse/intessa') ==
                u'https://github.com/dvxhouse/intessa?spam=eggs#foo')

    def test_with_query_replaces_query(self):
        assert (self.url.with_query('spam-ham-eggs') ==
                u'https://github.com/zacharyvoase/urlobject?spam-ham-eggs#foo')

    def test_without_query_removes_query(self):
        assert (self.url.without_query() ==
                u'https://github.com/zacharyvoase/urlobject#foo')

    def test_with_fragment_replaces_fragment(self):
        assert (self.url.with_fragment('part') ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs#part')

    def test_without_fragment_removes_fragment(self):
        assert (self.url.without_fragment() ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs')
