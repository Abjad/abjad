# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_list_unordered_named_pitch_pairs_in_expr_01():

    chord = Chord([0, 1, 2, 3], (1, 4))
    pairs = pitchtools.list_unordered_named_pitch_pairs_in_expr(chord)
    pairs = list(pairs)

    assert pairs[0] == (NamedPitch(0), NamedPitch(1))
    assert pairs[1] == (NamedPitch(0), NamedPitch(2))
    assert pairs[2] == (NamedPitch(0), NamedPitch(3))
    assert pairs[3] == (NamedPitch(1), NamedPitch(2))
    assert pairs[4] == (NamedPitch(1), NamedPitch(3))
    assert pairs[5] == (NamedPitch(2), NamedPitch(3))