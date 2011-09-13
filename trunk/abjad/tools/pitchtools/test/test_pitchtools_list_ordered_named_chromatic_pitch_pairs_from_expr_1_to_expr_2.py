from abjad import *


def test_pitchtools_list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2_01():

    chord_1 = Chord([0, 1, 2], (1, 4))
    chord_2 = Chord([3, 4], (1, 4))
    pairs = pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(chord_1, chord_2)
    pairs = list(pairs)

    assert pairs[0] == (pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(3))
    assert pairs[1] == (pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(4))
    assert pairs[2] == (pitchtools.NamedChromaticPitch(1), pitchtools.NamedChromaticPitch(3))
    assert pairs[3] == (pitchtools.NamedChromaticPitch(1), pitchtools.NamedChromaticPitch(4))
    assert pairs[4] == (pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(3))
    assert pairs[5] == (pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4))
