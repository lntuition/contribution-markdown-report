from attribute import Graph, Header, Summary


class Setting:
    pass


class HeaderSetting(Header, Setting):
    pass


class SummarySetting(Summary, Setting):
    pass


class GraphSetting(Graph, Setting):
    pass
