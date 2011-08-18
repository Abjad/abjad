from abjad.tools.intervaltreetools import BoundedInterval


def test_BoundedInterval___eq___01():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(0, 10)
    assert a == b


def test_BoundedInterval___eq___02():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(-1, 10)
    assert a != b


def test_BoundedInterval___eq___03():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(0, 11)
    assert a != b


def test_BoundedInterval___eq___04():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(0, 10, {})
    assert a == b


def test_BoundedInterval___eq___05():
    a = BoundedInterval(0, 10, {'animal': 'goose'})
    b = BoundedInterval(0, 10, {'animal': 'duck'})
    assert a != b
