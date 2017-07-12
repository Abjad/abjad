# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_NoteHead___setattr___01():
    r'''Slots constrain note-head attributes.
    '''

    note_head = abjad.NoteHead("cs''")

    assert pytest.raises(AttributeError, "note_head.foo = 'bar'")
