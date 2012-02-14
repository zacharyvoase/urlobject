import collections
import re
import urlparse


class QueryString(unicode):

    @property
    def list(self):
        result = []
        if not self:
            # Empty string => empty list.
            return result

        name_value_pairs = re.split(r'[\&\;]', self)
        for name_value_pair in name_value_pairs:
            # Split the pair string into a naive, encoded (name, value) pair.
            name_value = name_value_pair.split('=', 1)
            # 'param=' => ('param', None)
            if len(name_value) == 1:
                name, value = name_value + [None]
            # 'param=value' => ('param', 'value')
            # 'param=' => ('param', '')
            else:
                name, value = name_value

            decode = (lambda s: urlparse.unquote(str(s).replace('+', ' '))
                      .decode('utf-8'))
            name = decode(name)
            if value is not None:
                value = decode(value)

            result.append((name, value))
        return result

    @property
    def dict(self):
        return dict(self.list)

    @property
    def multi_dict(self):
        result = collections.defaultdict(list)
        for name, value in self.list:
            result[name].append(value)
        return dict(result)
