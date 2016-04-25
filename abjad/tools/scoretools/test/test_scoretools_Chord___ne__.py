# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___ne___01():

    chord_1 = Chord("<c' e' fs'>4")
    chord_2 = Chord("<c' e' fs'>4")
    chord_3 = Chord("<c' e' fs'>4")

    assert not chord_1 != chord_1
    assert     chord_1 != chord_2
    assert     chord_1 != chord_3
    assert     chord_2 != chord_1
    assert not chord_2 != chord_2
    assert     chord_2 != chord_3
    assert     chord_3 != chord_1
    assert     chord_3 != chord_2
    assert not chord_3 != chord_3
