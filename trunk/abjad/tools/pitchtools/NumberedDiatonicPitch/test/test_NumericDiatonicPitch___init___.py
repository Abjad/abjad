from abjad import *


def test_NumberedDiatonicPitch___init____01( ):

   numeric_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
   assert isinstance(numeric_diatonic_pitch, pitchtools.NumberedDiatonicPitch)


def test_NumberedDiatonicPitch___init____02( ):

   numeric_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
   numeric_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(numeric_diatonic_pitch_1)
   assert isinstance(numeric_diatonic_pitch_2, pitchtools.NumberedDiatonicPitch)
