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

def test__Interval___init____03( ):
    '''_Intervals can be instantiated from other intervals.'''
    i1 = _Interval(0, 10, 'data')
    i2 = _Interval(i1)
    assert i1.signature == i2.signature
    assert i1 != i2

def test__Interval___init____04( ):
    '''_Intervals can be instantiated with just a low and high value.'''
    i = _Interval(0, 10)

def test__Interval___init____05( ):
    '''_Intervals can be instantiated with 3 non-keyword arguments.'''
    i = _Interval(0, 10, 'data')

def test__Interval___init____06( ):
    '''_Intervals copy data on instantiation.'''
    data = { }
    i = _Interval(0, 10, data)
    data['cat'] = 'dog'
    assert data != i.data
