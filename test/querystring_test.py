# -*- coding: utf-8 -*-

import unittest

from urlobject.query_string import QueryString
from urlobject.six import u


class QueryStringTest(unittest.TestCase):

    def test_preserves_equality_with_original_string(self):
        assert QueryString('abc=123') == 'abc=123'

    def test_preserves_hash_value_of_original_string(self):
        assert hash(QueryString('abc=123')) == hash('abc=123')

    def test_list_returns_an_empty_list_for_empty_QueryStrings(self):
        assert QueryString('').list == []

    def test_list_correctly_splits_on_ampersands(self):
        assert QueryString('abc=123&def=456').list == [
            ('abc', '123'), ('def', '456')]

    def test_list_correctly_splits_on_semicolons(self):
        assert QueryString('abc=123;def=456').list == [
            ('abc', '123'), ('def', '456')]

    def test_list_correctly_decodes_special_chars(self):
        assert QueryString('a%20b=c%20d').list == [('a b', 'c d')]
        assert QueryString('a+b=c+d').list == [('a b', 'c d')]
        assert (QueryString('my%20weird%20field=q1!2%22\'w%245%267%2Fz8)%3F').list ==
                [('my weird field', 'q1!2"\'w$5&7/z8)?')])

    def test_list_correctly_decodes_utf_8(self):
        assert QueryString('foo=%EF%BF%BD').list == [('foo', u('\ufffd'))]

    def test_list_doesnt_split_on_percent_encoded_special_chars(self):
        assert QueryString('a%26b%3Dc%3F=a%26b%3Dc%3F').list == [
            ('a&b=c?', 'a&b=c?')]

    def test_list_doesnt_break_if_two_parameters_have_the_same_name(self):
        assert QueryString('abc=123;abc=456').list == [
            ('abc', '123'), ('abc', '456')]

    def test_list_uses_none_as_the_value_for_valueless_parameters(self):
        assert QueryString('abc').list == [('abc', None)]
        assert QueryString('abc=123&def&ghi=456').list == [
            ('abc', '123'), ('def', None), ('ghi', '456')]

    def test_list_uses_empty_string_for_empty_valued_parameters(self):
        assert QueryString('abc=').list == [('abc', '')]
        assert QueryString('abc=123&def=&ghi=456').list == [
            ('abc', '123'), ('def', ''), ('ghi', '456')]

    def test_list_uses_empty_string_for_anonymous_parameters(self):
        assert QueryString('=123').list == [('', '123')]
        assert QueryString('abc=123&=456&ghi=789').list == [
            ('abc', '123'), ('', '456'), ('ghi', '789')]

    def test_list_can_handle_void_parameters(self):
        assert QueryString('abc=123&&def=456').list == [
            ('abc', '123'), ('', None), ('def', '456')]
        assert QueryString('abc=123&=&def=456').list == [
            ('abc', '123'), ('', ''), ('def', '456')]

    def test_dict_returns_a_dictionary_with_one_value_per_key(self):
        assert QueryString('abc=123&abc=456').dict == {'abc': '456'}

    def test_multi_dict_returns_a_dictionary_with_all_values_per_key(self):
        assert QueryString('abc=123&abc=456').multi_dict == {
            'abc': ['123', '456']}

    def test_add_param_encodes_and_adds_the_given_parameter_to_the_QueryString(self):
        s = QueryString('')
        assert s.add_param('abc', '123') == 'abc=123'
        assert (s.add_param('abc', '123')
                 .add_param('def', '456') == 'abc=123&def=456')

    def test_add_param_can_add_valueless_parameters(self):
        s = QueryString('abc=123')
        assert s.add_param('def', None) == 'abc=123&def'

    def test_add_param_can_add_empty_valued_parameters(self):
        s = QueryString('abc=123')
        assert s.add_param('def', '') == 'abc=123&def='

    def test_add_param_can_add_anonymous_parameters(self):
        s = QueryString('abc=123')
        assert s.add_param('', '456') == 'abc=123&=456'

    def test_add_param_encodes_utf8(self):
        s = QueryString('abc=123')
        assert s.add_param('foo', u('\ufffd')) == 'abc=123&foo=%EF%BF%BD'

    def test_add_param_accepts_int(self):
        s = QueryString('')
        assert s.add_param('abc', 123) == 'abc=123'

    def test_add_param_allows_the_same_parameter_name_to_be_added_twice(self):
        s = QueryString('abc=123')
        assert s.add_param('abc', '456') == 'abc=123&abc=456'

    def test_add_param_encodes_special_characters(self):
        s = QueryString('abc=123')
        assert s.add_param('d e f', '4+5#6') == 'abc=123&d+e+f=4%2B5%236'

    def test_set_param_replaces_existing_parameter_names(self):
        s = QueryString('abc=123&abc=456')
        assert s.set_param('abc', '789') == 'abc=789'

    def test_del_param_removes_all_instances_of_the_parameter_from_the_QueryString(self):
        s = QueryString('abc=123&def=456&abc=789')
        assert s.del_param('abc') == 'def=456'
        assert s.del_param('def') == 'abc=123&abc=789'

    def test_del_param_can_remove_valueless_parameters(self):
        valueless = QueryString('abc=123&def&abc=456')
        empty_valued = QueryString('abc=123&def=&abc=456')
        assert valueless.del_param('def') == 'abc=123&abc=456'
        assert empty_valued.del_param('def') == 'abc=123&abc=456'

    def test_del_param_can_remove_anonymous_parameters(self):
        s = QueryString('abc=123&=456&def=789')
        assert s.del_param('') == 'abc=123&def=789'

    def test_add_params_is_equivalent_to_calling_add_param_multiple_times(self):
        s = QueryString('')
        assert (s.add_params([('abc', '123'), ('def', '456')]) ==
                s.add_param('abc', '123').add_param('def', '456'))

    def test_add_params_accepts_the_same_args_as_dict(self):
        s = QueryString('')
        added = s.add_params({'abc': '123'}, foo='bar', xyz='456')
        assert added.dict == {'abc': '123', 'foo': 'bar', 'xyz': '456'}
        added2 = s.add_params([('abc', '123')], foo='bar', xyz='456')
        assert added2.dict == {'abc': '123', 'foo': 'bar', 'xyz': '456'}
        # It also has to fail in the same way as `dict`. If you pass more than
        # one positional argument it should raise a TypeError.
        self.assertRaises(TypeError,
                          s.add_params, {'abc': '123'}, {'foo': 'bar'})

    def test_add_params_accepts_the_same_parameter_name_multiple_times(self):
        s = (QueryString('')
             .add_params([('abc', '123'), ('abc', '456')]))
        assert s.list == [('abc', '123'), ('abc', '456')]

    def test_add_params_with_multiple_values_adds_the_same_parameter_multiple_times(self):
        s = QueryString('')
        assert (s.add_params({'foo': ['bar', 'baz']}) ==
                s.add_param('foo', 'bar').add_param('foo', 'baz'))

    def test_set_params_is_equivalent_to_calling_set_param_multiple_times(self):
        s = QueryString('')
        assert (s.set_params([('abc', '123'), ('def', '456')]) ==
                s.set_param('abc', '123').set_param('def', '456'))

    def test_set_params_accepts_the_same_args_as_dict(self):
        s = QueryString('')
        added = s.set_params({'abc': '123'}, abc='456')
        assert added.dict == {'abc': '456'}
        added2 = s.set_params([('abc', '123')], abc='456')
        assert added2.dict == {'abc': '456'}

    def test_set_params_accepts_the_same_parameter_name_multiple_times(self):
        s = (QueryString('')
             .set_params([('abc', '123'), ('abc', '456')]))
        assert s.list == [('abc', '456')]

    def test_set_params_with_multiple_values_sets_the_same_name_multiple_times(self):
        s = QueryString('foo=spam')
        assert (s.set_params({'foo': ['bar', 'baz']}) ==
                'foo=bar&foo=baz')
        s2 = QueryString('foo=bar&foo=baz')
        assert (s2.set_params({'foo': ['spam', 'ham']}) ==
                'foo=spam&foo=ham')

    def test_del_params_accepts_an_iterable_and_removes_all_listed_parameters(self):
        s = QueryString('abc=123&def=456&xyz=789')
        assert s.del_params(('abc', 'xyz')) == 'def=456'

    def test_del_param_value_removes_the_specified_value_only(self):
        s = QueryString('abc=123&abc=456&def=789')
        assert s.del_param_value('abc', '456') == 'abc=123&def=789'
