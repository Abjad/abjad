from abjad import *


def test_pitchtools_list_unordered_named_chromatic_pitch_pairs_in_expr_01():

    chord = Chord([0, 1, 2, 3], (1, 4))
    pairs = pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(chord)
    pairs = list(pairs)

    assert pairs[0] == (pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(1))
    assert pairs[1] == (pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2))
    assert pairs[2] == (pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(3))
    assert pairs[3] == (pitchtools.NamedChromaticPitch(1), pitchtools.NamedChromaticPitch(2))
    assert pairs[4] == (pitchtools.NamedChromaticPitch(1), pitchtools.NamedChromaticPitch(3))
    assert pairs[5] == (pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(3))
