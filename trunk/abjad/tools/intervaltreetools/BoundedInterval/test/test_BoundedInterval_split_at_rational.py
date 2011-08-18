from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad import Fraction


def test_BoundedInterval_split_at_rational_01():
    '''BoundedInterval.split_at_rational returns a new BoundedInterval instance.'''
    i1 = BoundedInterval(3, 23)
    splits = i1.split_at_rational(13)
    assert splits[0].signature == (3, 13)
    assert splits[1].signature == (13, 23)

def test_BoundedInterval_split_at_rational_02():
    '''A split point at or outside the BoundedInterval bounds returns the original BoundedInterval.'''
    i1 = BoundedInterval(3, 23)
    splits = i1.split_at_rational(3)
    assert i1 == splits[0]
    splits = i1.split_at_rational(23)
    assert i1 == splits[0]
    splits = i1.split_at_rational(-1000)
    assert i1 == splits[0]
    splits = i1.split_at_rational(1000)
    assert i1 == splits[0]

def test_BoundedInterval_split_at_rational_03():
    '''BoundedIntervals can be split by Fractions.'''
    i1 = BoundedInterval(3, 23)
    splits = i1.split_at_rational(Fraction(46, 13))
    assert splits[0].signature == (3, Fraction(46, 13))
    assert splits[1].signature == (Fraction(46, 13), 23)
