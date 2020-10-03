from attribute import Graph, Header, Summary


def test_attribute_get_attribute() -> None:
    assert Header.get_attribute() == "Header"
    assert Summary.get_attribute() == "Summary"
    assert Graph.get_attribute() == "Graph"
