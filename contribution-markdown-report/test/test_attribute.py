from attribute import Attribute, Graph, Header, Summary


def test_attribute_get_attribute() -> None:
    assert Attribute.get_attribute() == "Attribute"
    assert Header.get_attribute() == "Header"
    assert Summary.get_attribute() == "Summary"
    assert Graph.get_attribute() == "Graph"
