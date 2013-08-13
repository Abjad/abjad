# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord___delitem___01():
    '''Deletes note head.
    '''

    chord = Chord("<ef' cs'' f''>4")
    del(chord[1])

    assert chord.lilypond_format == "<ef' f''>4"
