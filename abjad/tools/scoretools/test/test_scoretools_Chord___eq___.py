# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___eq____01():
    '''True only when chords have the same object ID.
    '''

    chord_1 = Chord([0, 4, 7], (1, 4))
    chord_2 = Chord([0, 4, 7], (1, 4))
    chord_3 = Chord([0, 4, 6], (1, 4))

    assert     chord_1 == chord_1
    assert not chord_1 == chord_2
    assert not chord_1 == chord_3
    assert not chord_2 == chord_1
    assert     chord_2 == chord_2
    assert not chord_2 == chord_3
    assert not chord_3 == chord_1
    assert not chord_3 == chord_2
    assert     chord_3 == chord_3
