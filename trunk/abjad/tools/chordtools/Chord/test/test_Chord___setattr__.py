from abjad import *
import py.test


def test_Chord___setattr___01():
    '''Slots constrain chord attributes.
    '''

    chord = Chord([3, 13, 17], (1, 4))

    assert py.test.raises(AttributeError, "chord.foo = 'bar'")
