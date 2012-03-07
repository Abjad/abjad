from abjad import *
import py.test


def test_LilyPondGrobOverrideComponentPlugIn___getattr___01():
    '''Getting unknown grob name raises exception.
    '''

    note = Note("c'8")
    assert py.test.raises(Exception, 'note.override.foo')
