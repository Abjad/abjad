from experimental import quantizationtools


def test_QGridLeaf___eq___01():

    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [])

    assert a == b


def test_QGridLeaf___eq___02():

    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [quantizationtools.SilentQEvent(1000)])
    c = quantizationtools.QGridLeaf(2, [])
    d = quantizationtools.QGridLeaf(2, [quantizationtools.SilentQEvent(1000)])

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
