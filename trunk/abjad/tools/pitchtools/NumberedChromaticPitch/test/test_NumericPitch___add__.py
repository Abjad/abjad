from abjad import *


def test_NumericPitch___add___01( ):
   '''Add numeric pitch to numeric pitch.'''

   p = pitchtools.NumberedChromaticPitch(12)
   q = pitchtools.NumberedChromaticPitch(13)

   assert p + q == pitchtools.NumberedChromaticPitch(25)


def test_NumericPitch___add___02( ):
   '''Add number to numeric pitch.'''

   p = pitchtools.NumberedChromaticPitch(12)

   assert p + 13 == pitchtools.NumberedChromaticPitch(25)
