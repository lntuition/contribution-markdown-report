from base.type import ConfigType


class HeaderGenerator():
    def _formatted_header(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def generate_header(self, username: str) -> str:
        return self._formatted_header(
            config={
                "username": username
            }
        )
