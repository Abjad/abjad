# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHead_tweak_01():

    chord = Chord([0, 2, 10], (1, 4))

    chord.note_heads[0].tweak.color = 'red'
    chord.note_heads[0].tweak.thickness = 2

    chord.note_heads[1].tweak.color = 'red'
    chord.note_heads[1].tweak.thickness = 2

    chord.note_heads[2].tweak.color = 'blue'

    tweak_reservoir_1 = chord.note_heads[0].tweak
    tweak_reservoir_2 = chord.note_heads[1].tweak
    tweak_reservoir_3 = chord.note_heads[2].tweak

    assert tweak_reservoir_1 == tweak_reservoir_1
    assert tweak_reservoir_1 == tweak_reservoir_2
    assert tweak_reservoir_1 != tweak_reservoir_3
    assert tweak_reservoir_2 == tweak_reservoir_1
    assert tweak_reservoir_2 == tweak_reservoir_2
    assert tweak_reservoir_2 != tweak_reservoir_3
    assert tweak_reservoir_3 != tweak_reservoir_1
    assert tweak_reservoir_3 != tweak_reservoir_2
    assert tweak_reservoir_3 == tweak_reservoir_3
