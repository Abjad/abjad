from abjad import *
import py.test


def test_Note___setattr___01():
    '''Slots constrain note attributes.
    '''

    note = Note("c'4")

    assert py.test.raises(AttributeError, "note.foo = 'bar'")
