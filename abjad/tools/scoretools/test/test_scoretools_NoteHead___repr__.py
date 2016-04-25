# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.scoretools import NoteHead


def test_scoretools_NoteHead___repr___01():
    r'''Note head repr is evaluable.
    '''

    note_head_1 = scoretools.NoteHead("cs''")
    note_head_2 = eval(repr(note_head_1))

    assert isinstance(note_head_1, scoretools.NoteHead)
    assert isinstance(note_head_2, scoretools.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
