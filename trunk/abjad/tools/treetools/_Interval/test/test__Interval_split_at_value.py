from fractions import Fraction
from abjad.tools.treetools._Interval import _Interval


def test__Interval_split_at_value_01( ):
    '''_Interval.split_at_value returns a new _Interval instance.'''
    i1 = _Interval(3, 23)
    splits = i1.split_at_value(13)
    assert splits[0].signature == (3, 13)
    assert splits[1].signature == (13, 23)
    
def test__Interval_split_at_value_02( ):
    '''A split point at or outside the _Interval bounds returns the original _Interval.'''
    i1 = _Interval(3, 23)
    splits = i1.split_at_value(3)
    assert i1 == splits
    splits = i1.split_at_value(23)
    assert i1 == splits
    splits = i1.split_at_value(-1000)
    assert i1 == splits
    splits = i1.split_at_value(1000)
    assert i1 == splits

def test__Interval_split_at_value_03( ):
    '''_Intervals can be split by Fractions.'''
    i1 = _Interval(3, 23)
    splits = i1.split_at_value(Fraction(46, 13))
    assert splits[0].signature == (3, Fraction(46, 13))
    assert splits[1].signature == (Fraction(46, 13), 23)
