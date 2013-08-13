# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord___getitem___01():
    '''Gets note head from chord.
    '''

    chord = Chord("<ef' cs'' f''>4")

    assert chord[0] is chord.note_heads[0]
    assert chord[1] is chord.note_heads[1]
    assert chord[2] is chord.note_heads[2]
