# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_NoteHead___setattr___01():
    r'''Slots constrain note head attributes.
    '''

    note_head = scoretools.NoteHead("cs''")

    assert pytest.raises(AttributeError, "note_head.foo = 'bar'")
