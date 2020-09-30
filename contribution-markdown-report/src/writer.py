from attribute import Graph, Header, Summary


class Writer:
    pass


class HeaderWriter(Header, Writer):
    pass


class SummaryWriter(Summary, Writer):
    pass


class GraphWriter(Graph, Writer):
    pass
