from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from fractions import Fraction


def test_TimeInterval_split_at_rationals_01():
    '''TimeInterval.split_at_rational returns a new TimeInterval instance.'''
    i1 = TimeInterval(3, 23)
    splits = i1.split_at_rationals(13)
    assert splits[0].signature == (3, 13)
    assert splits[1].signature == (13, 23)

def test_TimeInterval_split_at_rationals_02():
    '''A split point at or outside the TimeInterval bounds returns the original TimeInterval.'''
    i1 = TimeInterval(3, 23)
    splits = i1.split_at_rationals(3)
    assert i1 == splits[0]
    splits = i1.split_at_rationals(23)
    assert i1 == splits[0]
    splits = i1.split_at_rationals(-1000)
    assert i1 == splits[0]
    splits = i1.split_at_rationals(1000)
    assert i1 == splits[0]

def test_TimeInterval_split_at_rationals_03():
    '''TimeIntervals can be split by Fractions.'''
    i1 = TimeInterval(3, 23)
    splits = i1.split_at_rationals(Fraction(46, 13))
    assert splits[0].signature == (3, Fraction(46, 13))
    assert splits[1].signature == (Fraction(46, 13), 23)
