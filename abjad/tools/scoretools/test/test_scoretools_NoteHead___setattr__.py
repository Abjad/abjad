# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_NoteHead___setattr___01():
    r'''Slots constrain note head attributes.
    '''

    note_head = scoretools.NoteHead("cs''")

    assert pytest.raises(AttributeError, "note_head.foo = 'bar'")
