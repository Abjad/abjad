from abjad.tools.timeintervaltools import TimeInterval


def test_TimeInterval___eq___01():
    a = TimeInterval(0, 10)
    b = TimeInterval(0, 10)
    assert a == b


def test_TimeInterval___eq___02():
    a = TimeInterval(0, 10)
    b = TimeInterval(-1, 10)
    assert a != b


def test_TimeInterval___eq___03():
    a = TimeInterval(0, 10)
    b = TimeInterval(0, 11)
    assert a != b


def test_TimeInterval___eq___04():
    a = TimeInterval(0, 10)
    b = TimeInterval(0, 10, {})
    assert a == b


def test_TimeInterval___eq___05():
    a = TimeInterval(0, 10, {'animal': 'goose'})
    b = TimeInterval(0, 10, {'animal': 'duck'})
    assert a != b
