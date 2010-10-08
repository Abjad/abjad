from abjad import *


def test_NumberedDiatonicPitch_numeric_diatonic_pitch_class_01( ):

   numeric_diatonic_pitch = pitchtools.NumberedDiatonicPitch(-1)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(6)

   numeric_diatonic_pitch = pitchtools.NumberedDiatonicPitch(0)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(0)

   numeric_diatonic_pitch = pitchtools.NumberedDiatonicPitch(6)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(6)

   numeric_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumberedDiatonicPitchClass(0)
