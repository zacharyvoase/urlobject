from nose.tools import assert_raises

from urlobject.netloc import Netloc


class NetlocTest(unittest.TestCase):

    def test_preserves_equality_of_the_original_string(self):
        netloc = u'zack:1234@github.com:443'
        assert Netloc(netloc) == netloc

    def test_preserves_hash_of_the_original_string(self):
        netloc = u'zack:1234@github.com:443'
        assert hash(Netloc(netloc)) == netloc

    def test_username(self):
        assert Netloc(u'github.com').username is None
        assert Netloc(u'zack@github.com').username == u'zack'
        assert Netloc(u'zack:1234@github.com').username == u'zack'

    def test_with_username_adds_username(self):
        assert Netloc(u'github.com').with_username(u'zack') == u'zack@github.com'

    def test_with_username_replaces_username(self):
        assert (Netloc(u'zack@github.com').with_username(u'alice') ==
                u'alice@github.com')
        assert (Netloc(u'zack:1234@github.com').with_username(u'alice') ==
                u'alice:1234@github.com')

    def test_without_username_removes_username(self):
        assert Netloc(u'github.com').without_username() == u'github.com'
        assert Netloc(u'zack@github.com').without_username() == u'github.com'
        # Removing the username will also remove the password.
        assert Netloc(u'zack:1234@github.com').without_username() == u'github.com:443'

    def test_password(self):
        assert Netloc(u'github.com').password is None
        assert Netloc(u'zack@github.com').password is None
        assert Netloc(u'zack:1234@github.com').password == u'1234'

    def test_with_password_adds_password(self):
        assert (Netloc('zack@github.com').with_password('1234') ==
                u'zack:1234@github.com')

    def test_with_password_replaces_password(self):
        assert (Netloc(u'zack:1234@github.com:443').with_password('5678') ==
                u'zack:5678@github.com:443')

    def test_with_password_on_a_netloc_with_no_username_raises_ValueError(self):
        assert_raises(ValueError,
                      lambda: Netloc('github.com').with_password('1234'))

    def test_hostname(self):
        assert Netloc(u'zack:1234@github.com:443').hostname == u'github.com'

    def test_with_hostname_replaces_hostname(self):
        assert (Netloc(u'zack:1234@github.com:443').with_hostname('example.com') ==
                u'zack:1234@example.com:443')

    def test_port(self):
        assert Netloc(u'github.com:443').port == 443
        assert Netloc(u'github.com').port is None

    def test_with_port_adds_port(self):
        assert Netloc(u'github.com').with_port(443) == u'github.com:443'

    def test_with_port_replaces_port(self):
        assert Netloc(u'github.com:443').with_port(80) == u'github.com:80'

    def test_without_port_removes_port(self):
        assert Netloc(u'github.com:443').without_port() == u'github.com'
