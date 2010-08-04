from abjad import *


def test_Pitch_deviation_01( ):
   '''Deviation defaults to None.'''

   p = NamedPitch('bf', 4)
   assert p.deviation is None


def test_Pitch_deviation_02( ):
   '''Deviation can be int or float.'''

   p = NamedPitch('bf', 4)

   p.deviation = -31
   assert p.deviation == -31

   p.deviation = -12.4
   assert p.deviation == -12.4
