from abjad import *


def test_NamedPitch_deviation_01( ):
   '''Deviation defaults to None.'''

   p = pitchtools.NamedPitch('bf', 4)
   assert p.deviation is None


def test_NamedPitch_deviation_02( ):
   '''Deviation can be int or float.'''

   p = pitchtools.NamedPitch('bf', 4)

   p.deviation = -31
   assert p.deviation == -31

   p.deviation = -12.4
   assert p.deviation == -12.4
