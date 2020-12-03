
class Collection:

    def __init__(self, key, value):
        self.key = key,
        self.value = value

class QueryString:

    def __init__(self, query):
        assert isinstance(query, str)
        # Check that it's syntactically valid SQL
        self.query = query

class Table(Collection):

    def __init__(self, key, value):
        super().__init__(key, value)


class Channel(Collection):

    def __init__(self, key, value):
        assert '@' in key or any(['@' in k for k in key])
        super().__init__(key, value)


class View(QueryString):

    def __init__(self, query):
        super().__init__(query)
