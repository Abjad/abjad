from abjad import *
import py.test


def test__OffsetInterface___slots___01( ):
    '''Slots constrain offset interface attributes.
    '''

    note = Note("c'4")

    assert py.test.raises(AttributeError, "note._offset.foo = 'bar'")
