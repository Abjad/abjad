from experimental import quantizationtools


def test_QGridLeaf___eq___01():

    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [])

    assert a == b


def test_QGridLeaf___eq___02():

    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [quantizationtools.ProxyQEvent(quantizationtools.SilentQEvent(1000), 0.5)])
    c = quantizationtools.QGridLeaf(2, [])
    d = quantizationtools.QGridLeaf(2, [quantizationtools.ProxyQEvent(quantizationtools.SilentQEvent(1000), 0.5)])

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
