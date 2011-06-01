# -*- coding: utf-8 -*-

import doctest
import unittest

import urlobject
from urlobject import URLObject


class URLObjectTest(unittest.TestCase):

    def test_netloc(self):
        self.assertEqual(URLObject(host='example.com'), u'//example.com/')

    def test_scheme(self):
        self.assertEqual(URLObject(scheme='http', path='/hello/'), u'http:///hello/')
        self.assertEqual(URLObject(scheme='http', host='example.com'), u'http://example.com/')
        self.assertEqual(URLObject(scheme='', path='/hello/'), u'/hello/')

    def test_path(self):
        url = URLObject(path='/hello/')
        self.assertEqual(url, u'/hello/')
        # Using / operator syntax.
        self.assertEqual(url / 'foo', u'/hello/foo')
        # Two ways to do trailing slashes.
        self.assertEqual(url / 'foo/', u'/hello/foo/')
        self.assertEqual(url / 'foo' / '', u'/hello/foo/')

    def test_fragment(self):
        url = URLObject(path='/hello', fragment='world')
        self.assertEqual(url, u'/hello#world')
        self.assertEqual(url / 'fun', u'/hello/fun#world')

    def test_query(self):
        url = URLObject(scheme='http', host='www.google.com')
        url |= ('q', 'query')
        self.assertEqual(url, u'http://www.google.com/?q=query')
        self.assertEqual(url | ('q', 'another'), u'http://www.google.com/?q=another')
        self.assertEqual(url & ('q', 'another'), u'http://www.google.com/?q=query&q=another')

    def test_query_list(self):
        url = URLObject(scheme='http', host='www.google.com')
        url |= ('q', 'query')
        self.assertEqual(url.query_list(), [(u'q', u'query')])

        self.assertEqual(
            (url | ('q', 'another')).query_list(),
            [(u'q', u'another')])

        self.assertEqual(
            (url & ('q', 'another')).query_list(),
            [(u'q', u'query'), (u'q', u'another')])

    def test_query_dict_seq(self):
        url = URLObject(scheme='http', host='www.google.com')
        url |= ('q', 'query')
        self.assertEqual(url.query_dict(), {u'q': [u'query']})

        self.assertEqual(
            (url | ('q', 'another')).query_dict(),
            {u'q': [u'another']})

        self.assertEqual(
            (url & ('q', 'another')).query_dict(),
            {u'q': [u'query', u'another']})

    def test_query_dict_noseq(self):
        url = URLObject(scheme='http', host='www.google.com')
        url |= ('q', 'query')
        self.assertEqual(url.query_dict(seq=False), {u'q': u'query'})

        self.assertEqual(
            (url | ('q', 'another')).query_dict(seq=False),
            {u'q': u'another'})

        self.assertEqual(
            (url & ('q', 'another')).query_dict(seq=False),
            {u'q': u'another'})

    def test_unicode_query_strings(self):
        url = URLObject(scheme='http', host='example.com', path='/')
        url |= {'a': u'é'}
        self.assertEqual(str(url), 'http://example.com/?a=%C3%A9')
        url |= {'b': 'c'}
        self.assertEqual(str(url), 'http://example.com/?a=%C3%A9&b=c')


class URLObjectParseTest(unittest.TestCase):

    def setUp(self):
        self.url = URLObject.parse(u'http://www.google.com/search?q=something&hl=en#frag')

    def test_scheme(self):
        self.assertEqual(self.url.scheme, 'http')

    def test_host(self):
        self.assertEqual(self.url.host, 'www.google.com')

    def test_host_idna_encoding_is_parsed(self):
        url = URLObject.parse(u'http://xn--hllo-bpa.com/')
        self.assertEqual(url.host, u'héllo.com')

    def test_host_idna_encoding_is_preserved(self):
        url = URLObject.parse(u'http://xn--hllo-bpa.com/')
        self.assertEqual(unicode(url), u'http://xn--hllo-bpa.com/')

    def test_path(self):
        self.assertEqual(self.url.path, '/search')

    def test_path_is_not_double_escaped(self):
        url = URLObject.parse('http://www.google.com/path%20with%20spaces')
        self.assertEqual(unicode(url), 'http://www.google.com/path%20with%20spaces')
        self.assertEqual(url.path, '/path with spaces')

    def test_fragment(self):
        self.assertEqual(self.url.fragment, 'frag')

    def test_fragment_is_not_double_escaped(self):
        url = URLObject.parse('http://google.com/#frag%20with%20escapes')
        self.assertEqual(unicode(url), 'http://google.com/#frag%20with%20escapes')
        self.assertEqual(url.fragment, 'frag with escapes')

    def test_query(self):
        self.assertEqual(self.url.query, 'q=something&hl=en')

    def test_query_is_not_double_escaped(self):
        url = URLObject.parse('http://www.google.com/search?q=a%20string%20with%20escapes')
        self.assertEqual(unicode(url), 'http://www.google.com/search?q=a%20string%20with%20escapes')
        self.assertEqual(url.query, 'q=a%20string%20with%20escapes')

    def test_multiple_parses_are_idempotent(self):
        url = u'http://xn-hllo-bpa.com/path%20withspaces?query=es%25capes&foo=bar#frag%28withescapes%29'
        parse1 = URLObject.parse(url)
        self.assertEqual(unicode(url), unicode(parse1))
        parse2 = URLObject.parse(unicode(parse1))
        self.assertEqual(unicode(url), unicode(parse2))
        self.assertEqual(unicode(parse1), unicode(parse2))


if __name__ == '__main__':
    doctest.testmod(urlobject, optionflags=doctest.ELLIPSIS)
    unittest.main()
