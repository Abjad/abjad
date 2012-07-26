from experimental import quantizationtools


def test_QGridContainer___eq___01():

    a = quantizationtools.QGridContainer(1, [])
    b = quantizationtools.QGridContainer(1, [])

    assert a == b


def test_QGridContainer___eq___02():

    a = quantizationtools.QGridContainer(1, [
        quantizationtools.QGridLeaf(1)
        ])
    b = quantizationtools.QGridContainer(1, [
        quantizationtools.QGridLeaf(1)
        ])

    assert a == b


def test_QGridContainer___eq___03():

    a = quantizationtools.QGridContainer(1, [])
    b = quantizationtools.QGridContainer(2, [])
    c = quantizationtools.QGridContainer(1, [
        quantizationtools.QGridLeaf(1)
        ])
    d = quantizationtools.QGridContainer(2, [
        quantizationtools.QGridLeaf(1)
        ])
    e = quantizationtools.QGridContainer(2, [
        quantizationtools.QGridLeaf(2)
        ])

    assert a != b
    assert a != c
    assert a != d
    assert a != e

    assert b != c
    assert b != d
    assert b != e

    assert c != d
    assert c != e

    assert d != e


