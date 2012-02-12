from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
import py.test


def test_BoundedInterval___init___01():
    '''High offset must be greater than start offset.'''
    py.test.raises(AssertionError,
        "i = BoundedInterval(0, -10, 'this should fail.')")

def test_BoundedInterval___init___02():
    '''BoundedIntervals cannot be instantiated from floats.'''
    py.test.raises(AssertionError,
        "i = BoundedInterval(0.5, 2.3, 'this should fail.')")

def test_BoundedInterval___init___03():
    '''BoundedIntervals can be instantiated from other intervals.'''
    i1 = BoundedInterval(0, 10, {'hello': 'world!'})
    i2 = BoundedInterval(i1)
    assert i1 == i2
    assert i1 is not i2

def test_BoundedInterval___init___04():
    '''BoundedIntervals can be instantiated with just a start and stop offset.'''
    i = BoundedInterval(0, 10)

def test_BoundedInterval___init___05():
    '''BoundedIntervals can be instantiated with start offset, stop offset and dictionary.'''
    i = BoundedInterval(0, 10, {'hello': 'world!'})

def test_BoundedInterval___init___06():
    '''BoundedIntervals must take a dictionary as their data argument.'''
    py.test.raises(AssertionError,
        'i = BoundedInterval(0, 10, "nope")')

def test_BoundedInterval___init___07():
    '''BoundedIntervals copy data on instantiation.'''
    data = {}
    i = BoundedInterval(0, 10, data)
    data['cat'] = 'dog'
    assert data != i
