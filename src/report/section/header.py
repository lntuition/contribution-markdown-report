class HeaderGenerator():
    def _formatted_header(self, username: str) -> str:
        raise NotImplementedError()

    def generate_header(self, username: str) -> str:
        return self._formatted_header(username=username)
