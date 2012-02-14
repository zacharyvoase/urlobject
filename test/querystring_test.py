import unittest

from urlobject.query_string import QueryString


class QueryStringTest(unittest.TestCase):

    def test_preserves_equality_with_original_string(self):
        assert QueryString(u'abc=123') == u'abc=123'

    def test_preserves_hash_value_of_original_string(self):
        assert hash(QueryString(u'abc=123')) == hash(u'abc=123')

    def test_list_returns_an_empty_list_for_empty_QueryStrings(self):
        assert QueryString(u'').list == []

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

    def test_list_uses_none_as_the_value_for_valueless_parameters(self):
        assert QueryString(u'abc').list == [(u'abc', None)]
        assert QueryString(u'abc=123&def&ghi=456').list == [
            (u'abc', u'123'), (u'def', None), (u'ghi', u'456')]

    def test_list_uses_empty_string_for_empty_valued_parameters(self):
        assert QueryString(u'abc=').list == [(u'abc', u'')]
        assert QueryString(u'abc=123&def=&ghi=456').list == [
            (u'abc', u'123'), (u'def', u''), (u'ghi', u'456')]

    def test_list_uses_empty_string_for_anonymous_parameters(self):
        assert QueryString(u'=123').list == [(u'', u'123')]
        assert QueryString(u'abc=123&=456&ghi=789').list == [
            (u'abc', u'123'), (u'', u'456'), (u'ghi', u'789')]

    def test_list_can_handle_void_parameters(self):
        assert QueryString(u'abc=123&&def=456').list == [
            (u'abc', u'123'), (u'', None), (u'def', u'456')]
        assert QueryString(u'abc=123&=&def=456').list == [
            (u'abc', u'123'), (u'', u''), (u'def', u'456')]

    def test_dict_returns_a_dictionary_with_one_value_per_key(self):
        assert QueryString(u'abc=123&abc=456').dict == {u'abc': u'456'}

    def test_multi_dict_returns_a_dictionary_with_all_values_per_key(self):
        assert QueryString(u'abc=123&abc=456').multi_dict == {
            u'abc': [u'123', u'456']}

    def test_add_param_encodes_and_adds_the_given_parameter_to_the_QueryString(self):
        s = QueryString(u'')
        assert s.add_param(u'abc', u'123') == u'abc=123'
        assert (s.add_param(u'abc', u'123')
                 .add_param(u'def', u'456') == u'abc=123&def=456')

    def test_add_param_can_add_valueless_parameters(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'def', None) == u'abc=123&def'

    def test_add_param_can_add_empty_valued_parameters(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'def', u'') == u'abc=123&def='

    def test_add_param_can_add_anonymous_parameters(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'', u'456') == u'abc=123&=456'

    def test_add_param_encodes_utf8(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'foo', u'\ufffd') == u'abc=123&foo=%EF%BF%BD'

    def test_add_param_allows_the_same_parameter_name_to_be_added_twice(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'abc', u'456') == u'abc=123&abc=456'

    def test_add_param_encodes_special_characters(self):
        s = QueryString(u'abc=123')
        assert s.add_param(u'd e f', u'4+5#6') == u'abc=123&d%20e%20f=4%2B5%236'

    def test_set_param_replaces_existing_parameter_names(self):
        s = QueryString(u'abc=123&abc=456')
        assert s.set_param(u'abc', '789') == u'abc=789'

    def test_del_param_removes_all_instances_of_the_parameter_from_the_QueryString(self):
        s = QueryString(u'abc=123&def=456&abc=789')
        assert s.del_param(u'abc') == u'def=456'
        assert s.del_param(u'def') == u'abc=123&abc=789'

    def test_del_param_can_remove_valueless_parameters(self):
        valueless = QueryString(u'abc=123&def&abc=456')
        empty_valued = QueryString(u'abc=123&def=&abc=456')
        assert valueless.del_param(u'def') == u'abc=123&abc=456'
        assert empty_valued.del_param(u'def') == u'abc=123&abc=456'

    def test_del_param_can_remove_anonymous_parameters(self):
        s = QueryString(u'abc=123&=456&def=789')
        assert s.del_param(u'') == u'abc=123&def=789'

    def test_add_params_is_equivalent_to_calling_add_param_multiple_times(self):
        s = QueryString(u'')
        assert (s.add_params([(u'abc', u'123'), (u'def', u'456')]) ==
                s.add_param(u'abc', u'123').add_param(u'def', u'456'))

    def test_add_params_accepts_the_same_args_as_dict(self):
        s = QueryString(u'')
        added = s.add_params({u'abc': u'123'}, foo=u'bar', xyz='456')
        assert added.dict == {u'abc': u'123', u'foo': u'bar', u'xyz': u'456'}
        added2 = s.add_params([(u'abc', u'123')], foo=u'bar', xyz='456')
        assert added2.dict == {u'abc': u'123', u'foo': u'bar', u'xyz': u'456'}

    def test_add_params_accepts_the_same_parameter_name_multiple_times(self):
        s = (QueryString(u'')
             .add_params([(u'abc', u'123'), (u'abc', u'456')]))
        assert s.list == [(u'abc', u'123'), (u'abc', u'456')]

    def test_set_params_is_equivalent_to_calling_set_param_multiple_times(self):
        s = QueryString(u'')
        assert (s.set_params([(u'abc', u'123'), (u'def', u'456')]) ==
                s.set_param(u'abc', u'123').set_param(u'def', u'456'))

    def test_set_params_accepts_the_same_args_as_dict(self):
        s = QueryString(u'')
        added = s.set_params({u'abc': u'123'}, abc='456')
        assert added.dict == {u'abc': u'456'}
        added2 = s.set_params([(u'abc', u'123')], abc=u'456')
        assert added2.dict == {u'abc': u'456'}

    def test_set_params_accepts_the_same_parameter_name_multiple_times(self):
        s = (QueryString(u'')
             .set_params([(u'abc', u'123'), (u'abc', u'456')]))
        assert s.list == [(u'abc', u'456')]

    def test_del_params_accepts_an_iterable_and_removes_all_listed_parameters(self):
        s = QueryString(u'abc=123&def=456&xyz=789')
        assert s.del_params((u'abc', u'xyz')) == u'def=456'
