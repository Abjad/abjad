from abjad import *


def test_NumericPitch___add___01( ):
   '''Add numeric pitch to numeric pitch.'''

   p = pitchtools.NumericPitch(12)
   q = pitchtools.NumericPitch(13)

   assert p + q == pitchtools.NumericPitch(25)


def test_NumericPitch___add___02( ):
   '''Add number to numeric pitch.'''

   p = pitchtools.NumericPitch(12)

   assert p + 13 == pitchtools.NumericPitch(25)
