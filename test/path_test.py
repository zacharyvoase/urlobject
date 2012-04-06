# -*- coding: utf-8 -*-

import unittest

from urlobject.path import URLPath


class URLPathTest(unittest.TestCase):

    def test_preserves_equality_with_original_string(self):
        assert URLPath(u'/a/b/c') == u'/a/b/c'
        assert URLPath(u'a/b/c') == u'a/b/c'

    def test_root_always_returns_the_root_path(self):
        assert URLPath.root == u'/'
        assert URLPath(u'/').root == u'/'
        assert URLPath(u'/a/b/c').root == u'/'

    def test_preserves_hash_of_the_original_string(self):
        assert hash(URLPath(u'/a/b/c')) == hash(u'/a/b/c')

    def test_segments_breaks_the_path_into_segments(self):
        assert URLPath(u'/a/b/c').segments == (u'a', u'b', u'c')
        assert URLPath(u'/a/b/c/').segments == (u'a', u'b', u'c', u'')
        assert URLPath(u'a/b/c').segments == (u'a', u'b', u'c')

    def test_segments_decodes_percent_escapes(self):
        assert URLPath(u'/a%20b/c%2Fd/').segments == (u'a b', u'c/d', u'')

    def test_join_segments_joins_segments_into_a_single_path(self):
        URLPath.join_segments((u'a', u'b', u'c')) == u'/a/b/c'
        URLPath.join_segments((u'a', u'b', u'c', u'')) == u'/a/b/c/'

    def test_join_segments_can_create_relative_paths(self):
        URLPath.join_segments((u'a', u'b', u'c'), absolute=False) == u'a/b/c'
        URLPath.join_segments((u'a', u'b', u'c', u''), absolute=False) == u'a/b/c/'

    def test_join_segments_encodes_non_ascii_and_special_characters_including_slash(self):
        URLPath.join_segments((u'a b', u'd/é')) == u'/a%20b/d%2F%C3%A9'

    def test_is_leaf_node(self):
        assert URLPath(u'/a/b/c').is_leaf
        assert not URLPath(u'/a/b/c/').is_leaf

    def test_is_relative_equals_not_is_absolute(self):
        assert URLPath(u'a/b/c').is_relative
        assert not URLPath(u'/a/b/c').is_relative
        assert not URLPath(u'a/b/c').is_absolute
        assert URLPath(u'/a/b/c').is_absolute

    def test_parent_of_a_leaf_node(self):
        assert URLPath(u'/a/b/c').parent == u'/a/b/'

    def test_parent_of_a_non_leaf_node(self):
        assert URLPath(u'/a/b/c/').parent == u'/a/b/'

    def test_relative_on_a_leaf_node(self):
        path = URLPath(u'/a/b/c')
        assert path.relative(u'.') == u'/a/b/'
        assert path.relative(u'd') == u'/a/b/d'
        assert path.relative(u'..') == u'/a/'
        assert path.relative(u'../d') == u'/a/d'
        assert path.relative(u'/') == u'/'
        assert path.relative(u'/d') == u'/d'

    def test_relative_on_a_non_leaf_node(self):
        path = URLPath(u'/a/b/c/')
        assert path.relative(u'.') == u'/a/b/c/'
        assert path.relative(u'd') == u'/a/b/c/d'
        assert path.relative(u'..') == u'/a/b/'
        assert path.relative(u'../d') == u'/a/b/d'
        assert path.relative(u'/') == u'/'
        assert path.relative(u'/d') == u'/d'

    def test_add_segment_adds_path_segments_to_a_path(self):
        assert URLPath(u'').add_segment(u'a') == u'a'
        assert URLPath(u'/').add_segment(u'a') == u'/a'
        assert URLPath(u'/a/b/c').add_segment('d') == u'/a/b/c/d'
        assert URLPath(u'/a/b/c').add_segment('d/') == u'/a/b/c/d%2F'

    def test_add_segment_encodes_non_ascii_and_reserved_characters(self):
        assert URLPath(u'/a/b/c').add_segment(u'd é') == u'/a/b/c/d%20%C3%A9'

    def test_add_segment_encodes_slash_characters(self):
        assert URLPath(u'/a/b/c').add_segment(u'd/e') == u'/a/b/c/d%2Fe'

    def test_add_concatenates_whole_paths(self):
        assert URLPath(u'').add(u'a') == u'a'
        assert URLPath(u'/').add(u'a') == u'/a'
        assert URLPath(u'/a/b/c').add('d') == u'/a/b/c/d'
        assert URLPath(u'/a/b/c').add('d/') == u'/a/b/c/d/'
        assert URLPath(u'/a/b/c').add('d/e/f') == u'/a/b/c/d/e/f'

    def test_add_encodes_non_ascii_and_reserved_characters(self):
        assert URLPath(u'/a/b/c').add(u'd /é') == u'/a/b/c/d%20/%C3%A9'

    def test_add_does_not_encode_slash_characters(self):
        assert URLPath(u'/a/b/c').add(u'd/e') == u'/a/b/c/d/e'
