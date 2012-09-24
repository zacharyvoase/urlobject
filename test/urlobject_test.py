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


class URLObjectRelativeTest(unittest.TestCase):

    def setUp(self):
        self.url = URLObject(u"https://github.com/zacharyvoase/urlobject?spam=eggs#foo")

    def test_relative_with_scheme_returns_the_given_URL(self):
        assert self.url.relative(u'http://example.com/abc') == u'http://example.com/abc'

    def test_relative_with_netloc_returns_the_given_URL_but_preserves_scheme(self):
        assert self.url.relative(u'//example.com/abc') == u'https://example.com/abc'

    def test_relative_with_path_replaces_path_and_removes_query_string_and_fragment(self):
        assert self.url.relative(u'another-project') == u'https://github.com/zacharyvoase/another-project'
        assert self.url.relative(u'.') == u'https://github.com/zacharyvoase/'
        assert self.url.relative(u'/dvxhouse/intessa') == u'https://github.com/dvxhouse/intessa'
        assert self.url.relative(u'/dvxhouse/intessa') == u'https://github.com/dvxhouse/intessa'

    def test_relative_with_empty_string_removes_fragment_but_preserves_query(self):
        # The empty string is treated as a path meaning 'the current location'.
        assert self.url.relative('') == self.url.without_fragment()

    def test_relative_with_query_string_removes_fragment(self):
        assert self.url.relative('?name=value') == self.url.without_fragment().with_query('name=value')

    def test_relative_with_fragment_removes_nothing(self):
        assert self.url.relative('#foobar') == self.url.with_fragment('foobar')

    def test_compound_relative_urls(self):
        assert self.url.relative('//example.com/a/b') == u'https://example.com/a/b'
        assert self.url.relative('//example.com/a/b#bar') == u'https://example.com/a/b#bar'
        assert self.url.relative('//example.com/a/b?c=d#bar') == u'https://example.com/a/b?c=d#bar'
        assert self.url.relative('/a/b?c=d#bar') == u'https://github.com/a/b?c=d#bar'
        assert self.url.relative('?c=d#bar') == u'https://github.com/zacharyvoase/urlobject?c=d#bar'
        assert self.url.relative('#bar') == u'https://github.com/zacharyvoase/urlobject?spam=eggs#bar'



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

    def test_query_list_returns_a_list_of_query_params(self):
        assert self.url.query_list == [(u'spam', u'eggs')]

    def test_query_dict_returns_a_dict_of_query_params(self):
        assert self.url.query_dict == {u'spam': u'eggs'}

    def test_query_multi_dict_returns_a_multi_dict_of_query_params(self):
        url = URLObject(u'https://example.com/?spam=eggs&spam=ham&foo=bar')
        assert url.query_multi_dict == {u'spam': [u'eggs', u'ham'],
                                        u'foo': [u'bar']}

    def test_fragment_returns_fragment(self):
        assert self.url.fragment == u'foo'

    def test_fragment_is_decoded_correctly(self):
        url = URLObject(u'https://example.com/#frag%20ment')
        assert url.fragment == u'frag ment'

    def test_auth_properties_can_parse_username_and_password(self):
        url = URLObject(u'https://zack:12345@github.com/')
        assert url.username == u'zack'
        assert url.password == u'12345'
        assert url.auth == (u'zack', u'12345')

    def test_auth_properties_can_parse_username(self):
        url = URLObject(u'https://zack@github.com/')
        assert url.username == u'zack'
        assert url.password is None
        assert url.auth == (u'zack', None)

    def test_auth_properties_return_None_with_no_username_or_password(self):
        url = URLObject(u'https://github.com/')
        assert url.username is None
        assert url.password is None
        assert url.auth == (None, None)


class URLObjectModificationTest(unittest.TestCase):

    def setUp(self):
        self.url = URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_scheme_replaces_scheme(self):
        assert (self.url.with_scheme('http') ==
                u'http://github.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_netloc_replaces_netloc(self):
        assert (self.url.with_netloc('example.com') ==
                u'https://example.com/zacharyvoase/urlobject?spam=eggs#foo')

    def test_with_hostname_replaces_hostname(self):
        url = URLObject(u'https://user:pass@github.com/')
        assert (url.with_hostname('example.com') ==
                u'https://user:pass@example.com/')

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

    def test_root_goes_to_root_path(self):
        assert self.url.root == u'https://github.com/?spam=eggs#foo'

    def test_parent_jumps_up_one_level(self):
        url = URLObject(u'https://github.com/zacharyvoase/urlobject')
        assert url.parent == u'https://github.com/zacharyvoase/'
        assert url.parent.parent == u'https://github.com/'

    def test_add_path_segment_adds_a_path_segment(self):
        url = URLObject(u'https://github.com/zacharyvoase/urlobject')
        assert (url.add_path_segment('tree') ==
                u'https://github.com/zacharyvoase/urlobject/tree')
        assert (url.add_path_segment('tree/master') ==
                u'https://github.com/zacharyvoase/urlobject/tree%2Fmaster')

    def test_add_path_adds_a_partial_path(self):
        url = URLObject(u'https://github.com/zacharyvoase/urlobject')
        assert (url.add_path('tree') ==
                u'https://github.com/zacharyvoase/urlobject/tree')
        assert (url.add_path('tree/master') ==
                u'https://github.com/zacharyvoase/urlobject/tree/master')

    def test_is_leaf(self):
        assert URLObject(u'https://github.com/zacharyvoase/urlobject').is_leaf
        assert not URLObject(u'https://github.com/zacharyvoase/').is_leaf

    def test_with_query_replaces_query(self):
        assert (self.url.with_query('spam-ham-eggs') ==
                u'https://github.com/zacharyvoase/urlobject?spam-ham-eggs#foo')

    def test_without_query_removes_query(self):
        assert (self.url.without_query() ==
                u'https://github.com/zacharyvoase/urlobject#foo')

    def test_add_query_param_adds_one_query_parameter(self):
        assert (self.url.add_query_param(u'spam', u'ham') ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs&spam=ham#foo')

    def test_add_query_params_adds_multiple_query_parameters(self):
        assert (self.url.add_query_params([(u'spam', u'ham'), (u'foo', u'bar')]) ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs&spam=ham&foo=bar#foo')

    def test_set_query_param_adds_or_replaces_one_query_parameter(self):
        assert (self.url.set_query_param(u'spam', u'ham') ==
                u'https://github.com/zacharyvoase/urlobject?spam=ham#foo')

    def test_set_query_params_adds_or_replaces_multiple_query_parameters(self):
        assert (self.url.set_query_params({u'foo': u'bar'}, spam=u'ham') ==
                u'https://github.com/zacharyvoase/urlobject?foo=bar&spam=ham#foo')

    def test_set_query_params_with_multiple_values(self):
        assert (self.url.set_query_params({u'foo': [u'bar', 'baz']}) ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs&foo=bar&foo=baz#foo')

    def test_del_query_param_removes_one_query_parameter(self):
        assert (self.url.del_query_param(u'spam') ==
                u'https://github.com/zacharyvoase/urlobject#foo')

    def test_del_query_params_removes_multiple_query_parameters(self):
        url = URLObject(u'https://github.com/zacharyvoase/urlobject?foo=bar&baz=spam#foo')
        assert (url.del_query_params(['foo', 'baz']) ==
                u'https://github.com/zacharyvoase/urlobject#foo')

    def test_with_fragment_replaces_fragment(self):
        assert (self.url.with_fragment('part') ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs#part')

    def test_with_fragment_encodes_fragment_correctly(self):
        assert (self.url.with_fragment('foo bar#baz') ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo%20bar%23baz')

    def test_without_fragment_removes_fragment(self):
        assert (self.url.without_fragment() ==
                u'https://github.com/zacharyvoase/urlobject?spam=eggs')
