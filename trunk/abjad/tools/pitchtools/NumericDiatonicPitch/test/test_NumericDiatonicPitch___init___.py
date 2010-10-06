from abjad import *


def test_NumericDiatonicPitch___init____01( ):

   numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(7)
   assert isinstance(numeric_diatonic_pitch, pitchtools.NumericDiatonicPitch)


def test_NumericDiatonicPitch___init____02( ):

   numeric_diatonic_pitch_1 = pitchtools.NumericDiatonicPitch(7)
   numeric_diatonic_pitch_2 = pitchtools.NumericDiatonicPitch(numeric_diatonic_pitch_1)
   assert isinstance(numeric_diatonic_pitch_2, pitchtools.NumericDiatonicPitch)
