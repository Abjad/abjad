from abjad import *


def test_NumericDiatonicPitch_numeric_diatonic_pitch_class_01( ):

   numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(-1)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumericDiatonicPitchClass(6)

   numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(0)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumericDiatonicPitchClass(0)

   numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(6)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumericDiatonicPitchClass(6)

   numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(7)
   numeric_diatonic_pitch_class = numeric_diatonic_pitch.numeric_diatonic_pitch_class
   assert numeric_diatonic_pitch_class == pitchtools.NumericDiatonicPitchClass(0)
