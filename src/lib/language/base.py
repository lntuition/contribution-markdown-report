from lib.base.type import ConfigType


class LanguageSetting():
    def format_header(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def format_summary(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def config_graph(self) -> ConfigType:
        raise NotImplementedError()
