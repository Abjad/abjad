from abjad.tools import quantizationtools
import copy


def test_QGridLeaf___copy___01():

    leaf = quantizationtools.QGridLeaf(1)

    copied = copy.copy(leaf)

    assert leaf == copied
    assert leaf is not copied


def test_QGridLeaf___copy___02():

    leaf = quantizationtools.QGridLeaf(2, [
        quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1000), 0.5)
        ])

    copied = copy.copy(leaf)

    assert leaf == copied
    assert leaf is not copied
