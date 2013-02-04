# -*- coding: utf-8 -*-

import unittest

from urlobject.path import URLPath
from urlobject.six import u


class URLPathTest(unittest.TestCase):

    def test_preserves_equality_with_original_string(self):
        assert URLPath('/a/b/c') == '/a/b/c'
        assert URLPath('a/b/c') == 'a/b/c'

    def test_root_always_returns_the_root_path(self):
        assert URLPath.root == '/'
        assert URLPath('/').root == '/'
        assert URLPath('/a/b/c').root == '/'

    def test_preserves_hash_of_the_original_string(self):
        assert hash(URLPath('/a/b/c')) == hash('/a/b/c')

    def test_segments_breaks_the_path_into_segments(self):
        assert URLPath('/a/b/c').segments == ('a', 'b', 'c')
        assert URLPath('/a/b/c/').segments == ('a', 'b', 'c', '')
        assert URLPath('a/b/c').segments == ('a', 'b', 'c')

    def test_segments_decodes_percent_escapes(self):
        assert URLPath('/a%20b/c%2Fd/').segments == ('a b', 'c/d', '')

    def test_join_segments_joins_segments_into_a_single_path(self):
        assert URLPath.join_segments(('a', 'b', 'c')) == '/a/b/c'
        assert URLPath.join_segments(('a', 'b', 'c', '')) == '/a/b/c/'

    def test_join_segments_can_create_relative_paths(self):
        assert URLPath.join_segments(('a', 'b', 'c'), absolute=False) == 'a/b/c'
        assert URLPath.join_segments(('a', 'b', 'c', ''), absolute=False) == 'a/b/c/'

    def test_join_segments_encodes_non_ascii_and_special_characters_including_slash(self):
        assert URLPath.join_segments(('a b', u('d/\N{LATIN SMALL LETTER E WITH ACUTE}'))) == '/a%20b/d%2F%C3%A9'

    def test_is_leaf_node(self):
        assert URLPath('/a/b/c').is_leaf
        assert not URLPath('/a/b/c/').is_leaf

    def test_is_relative_equals_not_is_absolute(self):
        assert URLPath('a/b/c').is_relative
        assert not URLPath('/a/b/c').is_relative
        assert not URLPath('a/b/c').is_absolute
        assert URLPath('/a/b/c').is_absolute

    def test_parent_of_a_leaf_node(self):
        assert URLPath('/a/b/c').parent == '/a/b/'

    def test_parent_of_a_non_leaf_node(self):
        assert URLPath('/a/b/c/').parent == '/a/b/'

    def test_relative_on_a_leaf_node(self):
        path = URLPath('/a/b/c')
        assert path.relative('.') == '/a/b/'
        assert path.relative('d') == '/a/b/d'
        assert path.relative('..') == '/a/'
        assert path.relative('../d') == '/a/d'
        assert path.relative('/') == '/'
        assert path.relative('/d') == '/d'

    def test_relative_on_a_non_leaf_node(self):
        path = URLPath('/a/b/c/')
        assert path.relative('.') == '/a/b/c/'
        assert path.relative('d') == '/a/b/c/d'
        assert path.relative('..') == '/a/b/'
        assert path.relative('../d') == '/a/b/d'
        assert path.relative('/') == '/'
        assert path.relative('/d') == '/d'

    def test_add_segment_adds_path_segments_to_a_path(self):
        assert URLPath('').add_segment('a') == 'a'
        assert URLPath('/').add_segment('a') == '/a'
        assert URLPath('/a/b/c').add_segment('d') == '/a/b/c/d'
        assert URLPath('/a/b/c').add_segment('d/') == '/a/b/c/d%2F'

    def test_add_segment_encodes_non_ascii_and_reserved_characters(self):
        assert URLPath('/a/b/c').add_segment(u('d \N{LATIN SMALL LETTER E WITH ACUTE}')) == '/a/b/c/d%20%C3%A9'

    def test_add_segment_encodes_slash_characters(self):
        assert URLPath('/a/b/c').add_segment('d/e') == '/a/b/c/d%2Fe'

    def test_add_concatenates_whole_paths(self):
        assert URLPath('').add('a') == 'a'
        assert URLPath('/').add('a') == '/a'
        assert URLPath('/a/b/c').add('d') == '/a/b/c/d'
        assert URLPath('/a/b/c').add('d/') == '/a/b/c/d/'
        assert URLPath('/a/b/c').add('d/e/f') == '/a/b/c/d/e/f'

    def test_add_encodes_non_ascii_and_reserved_characters(self):
        assert URLPath('/a/b/c').add(u('d /\N{LATIN SMALL LETTER E WITH ACUTE}')) == '/a/b/c/d%20/%C3%A9'

    def test_add_does_not_encode_slash_characters(self):
        assert URLPath('/a/b/c').add('d/e') == '/a/b/c/d/e'
