from lib.base.type import ConfigType


class SectionGenerator():
    def configure(self) -> ConfigType:
        raise NotImplementedError()

    def process(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def generate(self) -> str:
        return self.process(
            config=self.configure()
        )
