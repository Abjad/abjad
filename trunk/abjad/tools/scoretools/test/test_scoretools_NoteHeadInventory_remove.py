# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Chord_remove_01():
    '''Remove note head from chord.
    '''

    chord = Chord("<ef' cs'' f''>4")
    note_head = chord[1]
    chord.remove(note_head)

    assert note_head._client is None
    assert chord.lilypond_format == "<ef' f''>4"
