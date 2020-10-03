from abc import ABC, abstractmethod


class Attribute(ABC):
    @staticmethod
    @abstractmethod
    def get_attribute() -> str:
        pass


class Header(Attribute):
    @staticmethod
    def get_attribute() -> str:
        return "Header"


class Summary(Attribute):
    @staticmethod
    def get_attribute() -> str:
        return "Summary"


class Graph(Attribute):
    @staticmethod
    def get_attribute() -> str:
        return "Graph"
