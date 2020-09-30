class Attribute:
    @classmethod
    def get_attribute(cls) -> str:
        return cls.__name__


class Header(Attribute):
    pass


class Summary(Attribute):
    pass


class Graph(Attribute):
    pass
