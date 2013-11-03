# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory_remove_01():
    '''Remove note head from chord.
    '''

    chord = Chord("<ef' cs'' f''>4")
    note_head = chord.note_heads[1]
    chord.note_heads.remove(note_head)

    assert note_head._client is None
    assert chord.lilypond_format == "<ef' f''>4"
