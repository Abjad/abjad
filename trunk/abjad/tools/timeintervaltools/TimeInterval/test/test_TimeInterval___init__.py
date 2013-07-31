from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
import py.test


def test_TimeInterval___init___01():
    r'''High offset must be greater than start_offset offset.
    '''
    py.test.raises(AssertionError,
        "i = TimeInterval(0, -10, 'this should fail.')")

def test_TimeInterval___init___02():
    r'''TimeIntervals cannot be instantiated from floats.
    '''
    py.test.raises(AssertionError,
        "i = TimeInterval(0.5, 2.3, 'this should fail.')")

def test_TimeInterval___init___03():
    r'''TimeIntervals can be instantiated from other intervals.
    '''
    i1 = TimeInterval(0, 10, {'hello': 'world!'})
    i2 = TimeInterval(i1)
    assert i1 == i2
    assert i1 is not i2

def test_TimeInterval___init___04():
    r'''TimeIntervals can be instantiated with just a start_offset and stop_offset offset.
    '''
    i = TimeInterval(0, 10)

def test_TimeInterval___init___05():
    r'''TimeIntervals can be instantiated with start_offset offset, stop_offset offset and dictionary.
    '''
    i = TimeInterval(0, 10, {'hello': 'world!'})

def test_TimeInterval___init___06():
    r'''TimeIntervals must take a dictionary as their data argument.
    '''
    py.test.raises(AssertionError,
        'i = TimeInterval(0, 10, "nope")')

def test_TimeInterval___init___07():
    r'''TimeIntervals copy data on instantiation.
    '''
    data = {}
    i = TimeInterval(0, 10, data)
    data['cat'] = 'dog'
    assert data != i
