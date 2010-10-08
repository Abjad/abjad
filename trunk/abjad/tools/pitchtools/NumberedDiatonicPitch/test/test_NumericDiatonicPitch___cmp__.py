from abjad import *


def test_NumberedDiatonicPitch___cmp___01( ):
   '''Compare equal numeric diatonic pitches.
   '''

   numeric_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
   numeric_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(7)

   assert     numeric_diatonic_pitch_1 == numeric_diatonic_pitch_2
   assert not numeric_diatonic_pitch_1 != numeric_diatonic_pitch_2
   assert not numeric_diatonic_pitch_1 <  numeric_diatonic_pitch_2
   assert     numeric_diatonic_pitch_1 <= numeric_diatonic_pitch_2
   assert not numeric_diatonic_pitch_1 >  numeric_diatonic_pitch_2
   assert     numeric_diatonic_pitch_1 >= numeric_diatonic_pitch_2


def test_NumberedDiatonicPitch___cmp___02( ):
   '''Compare numeric diatonic pitch to equivalent diatonic pitch number.
   '''

   numeric_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
   diatonic_pitch_number = 7

   assert     numeric_diatonic_pitch_1 == diatonic_pitch_number
   assert not numeric_diatonic_pitch_1 != diatonic_pitch_number
   assert not numeric_diatonic_pitch_1 <  diatonic_pitch_number
   assert     numeric_diatonic_pitch_1 <= diatonic_pitch_number
   assert not numeric_diatonic_pitch_1 >  diatonic_pitch_number
   assert     numeric_diatonic_pitch_1 >= diatonic_pitch_number


def test_NumberedDiatonicPitch___cmp___03( ):
   '''Compare unequal numeric diatonic pitches.
   '''

   numeric_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
   numeric_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(8)

   assert not numeric_diatonic_pitch_1 == numeric_diatonic_pitch_2
   assert     numeric_diatonic_pitch_1 != numeric_diatonic_pitch_2
   assert     numeric_diatonic_pitch_1 <  numeric_diatonic_pitch_2
   assert     numeric_diatonic_pitch_1 <= numeric_diatonic_pitch_2
   assert not numeric_diatonic_pitch_1 >  numeric_diatonic_pitch_2
   assert not numeric_diatonic_pitch_1 >= numeric_diatonic_pitch_2


def test_NumberedDiatonicPitch___cmp___04( ):
   '''Compare numeric diatonic pitches to inequivalent diatonic pitch number.
   '''

   numeric_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
   diatonic_pitch_number = 8

   assert not numeric_diatonic_pitch_1 == diatonic_pitch_number
   assert     numeric_diatonic_pitch_1 != diatonic_pitch_number
   assert     numeric_diatonic_pitch_1 <  diatonic_pitch_number
   assert     numeric_diatonic_pitch_1 <= diatonic_pitch_number
   assert not numeric_diatonic_pitch_1 >  diatonic_pitch_number
   assert not numeric_diatonic_pitch_1 >= diatonic_pitch_number
