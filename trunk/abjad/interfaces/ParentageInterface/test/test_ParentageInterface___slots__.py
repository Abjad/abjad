from abjad import *
import py.test


def test_ParentageInterface___slots___01( ):
    '''Slots constrain parentage interface attributes.
    '''

    note = Note("c'4")

    assert py.test.raises(AttributeError, "note.parentage.foo = 'bar'")
