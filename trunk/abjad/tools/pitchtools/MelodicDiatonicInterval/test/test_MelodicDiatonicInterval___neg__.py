from abjad import *


def test_MelodicDiatonicInterval___neg___01( ):

   interval = pitchtools.DiatonicInterval('minor', 3)
   assert -interval == pitchtools.DiatonicInterval('minor', -3)


def test_MelodicDiatonicInterval___neg___02( ):

   interval = pitchtools.DiatonicInterval('minor', -3)
   assert -interval == pitchtools.DiatonicInterval('minor', 3)
