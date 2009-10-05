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
    
    def test_path(self):
        self.assertEqual(self.url.path, '/search')
    
    def test_fragment(self):
        self.assertEqual(self.url.fragment, 'frag')
    
    def test_query(self):
        self.assertEqual(self.url.query, 'q=something&hl=en')


if __name__ == '__main__':
    doctest.testmod(urlobject, optionflags=doctest.ELLIPSIS)
    unittest.main()
