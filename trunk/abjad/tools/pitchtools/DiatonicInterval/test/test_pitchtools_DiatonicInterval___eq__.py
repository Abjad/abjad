from abjad import *
import py.test
py.test.skip( )


def test_pitchtools_DiatonicInterval___eq___01( ):

   diatonic_interval_1 = pitchtools.DiatonicInterval('minor', 2)
   diatonic_interval_2 = pitchtools.DiatonicInterval('minor', 2)
   
   assert diatonic_interval_1 == diatonic_interval_2


def test_pitchtools_DiatonicInterval___eq___02( ):

   diatonic_interval_1 = pitchtools.DiatonicInterval('minor', 2)
   diatonic_interval_2 = pitchtools.DiatonicInterval('augmented', 1)
   
   assert not diatonic_interval_1 == diatonic_interval_2
