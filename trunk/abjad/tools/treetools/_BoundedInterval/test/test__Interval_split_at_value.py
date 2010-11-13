from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_split_at_value_01( ):
    '''_BoundedInterval.split_at_value returns a new _BoundedInterval instance.'''
    i1 = _BoundedInterval(3, 23)
    splits = i1.split_at_value(13)
    assert splits[0].signature == (3, 13)
    assert splits[1].signature == (13, 23)
    
def test__BoundedInterval_split_at_value_02( ):
    '''A split point at or outside the _BoundedInterval bounds returns the original _BoundedInterval.'''
    i1 = _BoundedInterval(3, 23)
    splits = i1.split_at_value(3)
    assert i1 == splits
    splits = i1.split_at_value(23)
    assert i1 == splits
    splits = i1.split_at_value(-1000)
    assert i1 == splits
    splits = i1.split_at_value(1000)
    assert i1 == splits

def test__BoundedInterval_split_at_value_03( ):
    '''_BoundedIntervals can be split by Fractions.'''
    i1 = _BoundedInterval(3, 23)
    splits = i1.split_at_value(Fraction(46, 13))
    assert splits[0].signature == (3, Fraction(46, 13))
    assert splits[1].signature == (Fraction(46, 13), 23)
