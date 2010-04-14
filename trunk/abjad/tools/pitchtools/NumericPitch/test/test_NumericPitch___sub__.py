from abjad import *


def test_NumericPitch___sub___01( ):
   '''Subtract numeric pitch from numeric pitch.'''

   p = pitchtools.NumericPitch(12)
   q = pitchtools.NumericPitch(13)

   assert p - q == pitchtools.NumericPitch(-1)
   assert q - p == pitchtools.NumericPitch(1)


def test_NumericPitch___sub___02( ):
   '''Subtract number from numeric pitch.'''

   p = pitchtools.NumericPitch(12)

   assert p - 13 == pitchtools.NumericPitch(-1)
