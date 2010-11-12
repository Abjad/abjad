import py.test
from abjad.tools.treetools._Interval import _Interval


def test__Interval___init____01( ):
    '''High value must be greater than or equal to low value.'''
    py.test.raises(AssertionError,
        "i = _Interval(0, -10, 'this should fail.')")


def test__Interval___init____02( ):
    '''_Intervals cannot be instantiated from floats.'''
    py.test.raises(AssertionError,
        "i = _Interval(0.5, 2.3, 'this should fail.')")
