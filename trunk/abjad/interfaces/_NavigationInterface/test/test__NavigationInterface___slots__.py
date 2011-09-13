from abjad import *
import py.test


def test__NavigationInterface___slots___01( ):
    '''Slots constrain navigation interface.
    '''

    note = Note("c'4")

    assert py.test.raises(AttributeError, "note._navigator.foo = 'bar'")
