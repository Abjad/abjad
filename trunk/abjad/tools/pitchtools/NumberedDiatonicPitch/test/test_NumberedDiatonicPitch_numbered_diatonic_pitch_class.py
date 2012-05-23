from abjad import *


def test_NumberedDiatonicPitch_numbered_diatonic_pitch_class_01():

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(-1)
    numbered_diatonic_pitch_class = numbered_diatonic_pitch.numbered_diatonic_pitch_class
    assert numbered_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(6)

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(0)
    numbered_diatonic_pitch_class = numbered_diatonic_pitch.numbered_diatonic_pitch_class
    assert numbered_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(0)

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(6)
    numbered_diatonic_pitch_class = numbered_diatonic_pitch.numbered_diatonic_pitch_class
    assert numbered_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(6)

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
    numbered_diatonic_pitch_class = numbered_diatonic_pitch.numbered_diatonic_pitch_class
    assert numbered_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(0)
