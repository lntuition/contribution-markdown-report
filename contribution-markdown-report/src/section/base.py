from abc import ABC, abstractmethod


class Section(ABC):
    @abstractmethod
    def write(self) -> str:
        pass
