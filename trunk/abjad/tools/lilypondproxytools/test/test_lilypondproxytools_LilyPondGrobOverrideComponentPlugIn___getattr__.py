# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_lilypondproxytools_LilyPondGrobOverrideComponentPlugIn___getattr___01():
    r'''Getting unknown grob name raises exception.
    '''

    note = Note("c'8")
    assert py.test.raises(Exception, 'note.override.foo')
