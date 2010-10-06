from abjad import *


def test_NamedDiatonicPitch___eq___01( ):

   named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
   named_diatonic_pitch_2 = pitchtools.NamedDiatonicPitch("c''")
   named_diatonic_pitch_3 = pitchtools.NamedDiatonicPitch("d''")

   assert     named_diatonic_pitch_1 == named_diatonic_pitch_1
   assert     named_diatonic_pitch_1 == named_diatonic_pitch_2
   assert not named_diatonic_pitch_1 == named_diatonic_pitch_3
   assert     named_diatonic_pitch_2 == named_diatonic_pitch_1
   assert     named_diatonic_pitch_2 == named_diatonic_pitch_2
   assert not named_diatonic_pitch_2 == named_diatonic_pitch_3
   assert not named_diatonic_pitch_3 == named_diatonic_pitch_1
   assert not named_diatonic_pitch_3 == named_diatonic_pitch_2
   assert     named_diatonic_pitch_3 == named_diatonic_pitch_3


def test_NamedDiatonicPitch___eq___02( ):

   assert pitchtools.NamedDiatonicPitch("c''") == 7
