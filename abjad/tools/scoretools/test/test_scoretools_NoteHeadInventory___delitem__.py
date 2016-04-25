# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory___delitem___01():
    '''Deletes note head.
    '''

    chord = Chord("<ef' cs'' f''>4")
    del(chord.note_heads[1])

    assert format(chord) == "<ef' f''>4"
