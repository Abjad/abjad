# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_lilypondproxytools_LilyPondGrobOverrideComponentPlugIn___getattr___01():
    r'''Getting unknown grob name raises exception.
    '''

    note = Note("c'8")
    assert py.test.raises(Exception, 'override(note).foo')
