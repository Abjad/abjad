# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord_pop_01():

    chord = Chord("<ef' cs'' f''>4")
    note_head = chord.pop(1)

    assert note_head._client is None
    assert chord.lilypond_format == "<ef' f''>4"
