import py.test
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval___init____01( ):
    '''High value must be greater than or equal to low value.'''
    py.test.raises(AssertionError,
        "i = _BoundedInterval(0, -10, 'this should fail.')")

def test__BoundedInterval___init____02( ):
    '''_BoundedIntervals cannot be instantiated from floats.'''
    py.test.raises(AssertionError,
        "i = _BoundedInterval(0.5, 2.3, 'this should fail.')")

def test__BoundedInterval___init____03( ):
    '''_BoundedIntervals can be instantiated from other intervals.'''
    i1 = _BoundedInterval(0, 10, 'data')
    i2 = _BoundedInterval(i1)
    assert i1.signature == i2.signature
    assert i1 != i2

def test__BoundedInterval___init____04( ):
    '''_BoundedIntervals can be instantiated with just a low and high value.'''
    i = _BoundedInterval(0, 10)

def test__BoundedInterval___init____05( ):
    '''_BoundedIntervals can be instantiated with 3 non-keyword arguments.'''
    i = _BoundedInterval(0, 10, 'data')

def test__BoundedInterval___init____06( ):
    '''_BoundedIntervals copy data on instantiation.'''
    data = { }
    i = _BoundedInterval(0, 10, data)
    data['cat'] = 'dog'
    assert data != i.data
