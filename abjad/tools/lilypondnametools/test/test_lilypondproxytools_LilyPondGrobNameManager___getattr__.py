# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_lilypondproxytools_LilyPondGrobNameManager___getattr___01():
    r'''Getting unknown grob name raises exception.
    '''

    note = Note("c'8")
    assert pytest.raises(Exception, 'override(note).foo')
