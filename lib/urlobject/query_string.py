import collections
import urlparse


class QueryString(unicode):

    @property
    def list(self):
        return urlparse.parse_qsl(self.encode('utf-8'))

    @property
    def dict(self):
        return dict(self.list)

    @property
    def multi_dict(self):
        result = collections.defaultdict(list)
        for name, value in self.list:
            result[name].append(value)
        return dict(result)
