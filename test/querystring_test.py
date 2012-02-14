import unittest

from urlobject.query_string import QueryString


class QueryStringTest(unittest.TestCase):

    def test_preserves_equality_with_original_string(self):
        assert QueryString(u'abc=123') == u'abc=123'

    def test_preserves_hash_value_of_original_string(self):
        assert hash(QueryString(u'abc=123')) == hash(u'abc=123')

    def test_list_correctly_splits_on_ampersands(self):
        assert QueryString(u'abc=123&def=456').list == [
            (u'abc', u'123'), (u'def', u'456')]

    def test_list_correctly_splits_on_semicolons(self):
        assert QueryString(u'abc=123;def=456').list == [
            (u'abc', u'123'), (u'def', u'456')]

    def test_list_correctly_decodes_special_chars(self):
        assert QueryString(u'a%20b=c%20d').list == [(u'a b', u'c d')]
        assert QueryString(u'a+b=c+d').list == [(u'a b', u'c d')]
        assert (QueryString(u'my%20weird%20field=q1!2%22\'w%245%267%2Fz8)%3F').list ==
                [(u'my weird field', u'q1!2"\'w$5&7/z8)?')])

    def test_list_correctly_decodes_utf_8(self):
        assert QueryString(u'foo=%EF%BF%BD').list == [(u'foo', u'\ufffd')]

    def test_list_doesnt_split_on_percent_encoded_special_chars(self):
        assert QueryString(u'a%26b%3Dc%3F=a%26b%3Dc%3F').list == [
            (u'a&b=c?', u'a&b=c?')]

    def test_list_doesnt_break_if_two_parameters_have_the_same_name(self):
        assert QueryString(u'abc=123;abc=456').list == [
            (u'abc', u'123'), (u'abc', u'456')]

    def test_list_returns_none_as_the_value_for_valueless_parameters(self):
        assert QueryString(u'abc').list == [(u'abc', None)]
        assert QueryString(u'abc=123&def&ghi=456').list == [
            (u'abc', u'123'), (u'def', None), (u'ghi', u'456')]

    def test_list_returns_empty_string_for_empty_valued_parameters(self):
        assert QueryString(u'abc=').list == [(u'abc', u'')]
        assert QueryString(u'abc=123&def=&ghi=456').list == [
            (u'abc', u'123'), (u'def', u''), (u'ghi', u'456')]

    def test_list_returns_empty_string_for_empty_named_parameters(self):
        assert QueryString(u'=123').list == [(u'', u'123')]
        assert QueryString(u'abc=123&=456&ghi=789').list == [
            (u'abc', u'123'), (u'', u'456'), (u'ghi', u'789')]

    def test_dict_returns_a_dictionary_with_one_value_per_key(self):
        assert QueryString(u'abc=123&abc=456').dict == {u'abc': u'456'}

    def test_multi_dict_returns_a_dictionary_with_all_values_per_key(self):
        assert QueryString(u'abc=123&abc=456').multi_dict == {
            u'abc': [u'123', u'456']}
