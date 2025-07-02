import unittest

from pytest import raises

from urlobject.netloc import Netloc


class NetlocTest(unittest.TestCase):

    def test_preserves_equality_of_the_original_string(self):
        netloc = 'zack:1234@github.com:443'
        assert Netloc(netloc) == netloc

    def test_preserves_hash_of_the_original_string(self):
        netloc = 'zack:1234@github.com:443'
        assert hash(Netloc(netloc)) == hash(netloc)

    def test_username(self):
        assert Netloc('github.com').username is None
        assert Netloc('zack@github.com').username == 'zack'
        assert Netloc('zack:1234@github.com').username == 'zack'

    def test_with_username_adds_username(self):
        assert Netloc('github.com').with_username('zack') == 'zack@github.com'

    def test_with_username_replaces_username(self):
        assert (Netloc('zack@github.com').with_username('alice') ==
                'alice@github.com')
        assert (Netloc('zack:1234@github.com').with_username('alice') ==
                'alice:1234@github.com')

    def test_without_username_removes_username(self):
        assert Netloc('github.com').without_username() == 'github.com'
        assert Netloc('zack@github.com').without_username() == 'github.com'
        # Removing the username will also remove the password.
        assert Netloc('zack:1234@github.com:443').without_username() == 'github.com:443'

    def test_password(self):
        assert Netloc('github.com').password is None
        assert Netloc('zack@github.com').password is None
        assert Netloc('zack:1234@github.com').password == '1234'

    def test_with_password_adds_password(self):
        assert (Netloc('zack@github.com').with_password('1234') ==
                'zack:1234@github.com')

    def test_with_password_replaces_password(self):
        assert (Netloc('zack:1234@github.com:443').with_password('5678') ==
                'zack:5678@github.com:443')

    def test_with_password_on_a_netloc_with_no_username_raises_ValueError(self):
        raises(ValueError,
               lambda: Netloc('github.com').with_password('1234'))

    def test_with_auth_with_one_arg_adds_username(self):
        assert (Netloc('github.com').with_auth('zack') ==
                'zack@github.com')

    def test_auth(self):
        assert Netloc('github.com').auth == (None, None)
        assert Netloc('zack@github.com').auth == ('zack', None)
        assert Netloc('zack:1234@github.com').auth == ('zack', '1234')

    def test_with_auth_with_one_arg_replaces_whole_auth_string_with_username(self):
        assert (Netloc('alice:1234@github.com').with_auth('zack') ==
                'zack@github.com')

    def test_with_auth_with_two_args_adds_username_and_password(self):
        assert (Netloc('github.com').with_auth('zack', '1234') ==
                'zack:1234@github.com')

    def test_with_auth_with_two_args_replaces_whole_auth_string_with_username_and_password(self):
        # Replaces username-only auth string
        assert (Netloc('alice@github.com').with_auth('zack', '1234') ==
                'zack:1234@github.com')

        # Replaces username and password.
        assert (Netloc('alice:4567@github.com').with_auth('zack', '1234') ==
                'zack:1234@github.com')

    def test_without_auth_removes_entire_auth_string(self):
        # No username or password => no-op.
        netloc = Netloc('github.com')
        assert netloc.without_auth() == 'github.com'
        # Username-only.
        netloc = Netloc('alice@github.com')
        assert netloc.without_auth() == 'github.com'
        # Username and password.
        netloc = Netloc('alice:1234@github.com')
        assert netloc.without_auth() == 'github.com'

    def test_hostname(self):
        assert Netloc('zack:1234@github.com:443').hostname == 'github.com'

    def test_with_hostname_replaces_hostname(self):
        assert (Netloc('zack:1234@github.com:443').with_hostname('example.com') ==
                'zack:1234@example.com:443')

    def test_port(self):
        assert Netloc('github.com:443').port == 443
        assert Netloc('github.com').port is None

    def test_with_port_adds_port(self):
        assert Netloc('github.com').with_port(443) == 'github.com:443'

    def test_with_port_replaces_port(self):
        assert Netloc('github.com:443').with_port(80) == 'github.com:80'

    def test_without_port_removes_port(self):
        assert Netloc('github.com:443').without_port() == 'github.com'
