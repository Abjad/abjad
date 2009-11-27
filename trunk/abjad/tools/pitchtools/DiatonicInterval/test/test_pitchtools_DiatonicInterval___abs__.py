from abjad import *


def test_pitchtools_DiatonicInterval___abs___01( ):

   interval = pitchtools.DiatonicInterval('minor', 3)
   assert abs(interval) == pitchtools.DiatonicInterval('minor', 3)


def test_pitchtools_DiatonicInterval___abs___02( ):

   interval = pitchtools.DiatonicInterval('minor', -3)
   assert abs(interval) == pitchtools.DiatonicInterval('minor', 3)
