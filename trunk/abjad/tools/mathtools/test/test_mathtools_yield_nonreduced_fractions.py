from abjad import *
from abjad.tools import durationtools


def test_mathtools_yield_nonreduced_fractions_01():

    generator = mathtools.yield_nonreduced_fractions()

    assert generator.next() == (1, 1)
    assert generator.next() == (2, 1)
    assert generator.next() == (1, 2)
    assert generator.next() == (1, 3)
    assert generator.next() == (2, 2)
    assert generator.next() == (3, 1)
    assert generator.next() == (4, 1)
    assert generator.next() == (3, 2)
    assert generator.next() == (2, 3)
    assert generator.next() == (1, 4)
    assert generator.next() == (1, 5)
    assert generator.next() == (2, 4)
