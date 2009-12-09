from abjad import *


def test_HarmonicDiatonicIntervalClass___init__01( ):
   '''Unisons and octaves are treated differently.'''

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)
   assert str(hdic) == 'P1'
   assert hdic.number == 1

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -1)
   assert str(hdic) == 'P1'
   assert hdic.number == 1


def test_HarmonicDiatonicIntervalClass___init__02( ):
   '''Unisons and octaves are treated differently.'''

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -15)
   assert str(hdic) == 'P8'
   assert hdic.number == 8

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', -8)
   assert str(hdic) == 'P8'
   assert hdic.number == 8

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)
   assert str(hdic) == 'P8'
   assert hdic.number == 8

   hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 15)
   assert str(hdic) == 'P8'
   assert hdic.number == 8
