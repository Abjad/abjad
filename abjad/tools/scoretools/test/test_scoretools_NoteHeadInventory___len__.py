# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory___len___01():

    assert len(Chord('<>4').note_heads) == 0
    assert len(Chord("<ef'>4").note_heads) == 1
    assert len(Chord("<ef' cs''>4").note_heads) == 2
    assert len(Chord("<ef' cs'' f''>4").note_heads) == 3
