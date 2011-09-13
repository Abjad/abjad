from abjad import *


def test_pitchtools_all_are_chromatic_pitch_class_name_octave_number_pairs_01():

    assert pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs(
        [('c', 4), ('d', 4), pitchtools.NamedChromaticPitch('e', 4)])
    assert pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs([0, 2, 4])
    assert not pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs(['foo', 'bar'])
