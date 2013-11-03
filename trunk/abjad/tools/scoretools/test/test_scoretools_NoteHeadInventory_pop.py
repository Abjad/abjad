# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory_pop_01():
    '''Pop note head from chord.
    '''

    chord = Chord("<ef' cs'' f''>4")
    note_head = chord.note_heads.pop(1)

    assert note_head._client is None
    assert chord.lilypond_format == "<ef' f''>4"
