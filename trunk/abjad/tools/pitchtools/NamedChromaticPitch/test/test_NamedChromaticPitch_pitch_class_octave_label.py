from abjad import *


def test_NamedChromaticPitch_pitch_class_octave_label_01():

    named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
    assert named_chromatic_pitch.pitch_class_octave_label == 'C#5'
