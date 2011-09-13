from abjad import *


def test_pitchtools_is_chromatic_pitch_class_name_octave_number_pair_01():

    assert pitchtools.is_chromatic_pitch_class_name_octave_number_pair(('c', 4))
    assert pitchtools.is_chromatic_pitch_class_name_octave_number_pair(('cs', 4))
    assert not pitchtools.is_chromatic_pitch_class_name_octave_number_pair('cs4')
