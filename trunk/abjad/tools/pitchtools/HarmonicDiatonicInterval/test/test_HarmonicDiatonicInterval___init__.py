from abjad import *


def test_HarmonicDiatonicInterval___init__01( ):
   '''Can init from quality string and interval number.'''

   hdi = pitchtools.HarmonicDiatonicInterval('major', 3)

   assert hdi.quality_string == 'major'
   assert hdi.interval_number == 3


def test_HarmonicDiatonicInterval___init__02( ):
   '''Can init from other harmonic diatonic interval.'''

   hdi = pitchtools.HarmonicDiatonicInterval('major', 3)
   new = pitchtools.HarmonicDiatonicInterval(hdi)

   assert hdi.quality_string == 'major'
   assert hdi.interval_number == 3

   assert new.quality_string == 'major'
   assert new.interval_number == 3

   assert new is not hdi   
   assert new == hdi


def test_HarmonicDiatonicInterval___init__03( ):
   '''Can init from melodic diatonic interval.'''

   mdi = pitchtools.MelodicDiatonicInterval('major', -3)
   hdi = pitchtools.HarmonicDiatonicInterval(mdi)

   assert mdi.quality_string == 'major'
   assert mdi.interval_number == -3

   assert hdi.quality_string == 'major'
   assert hdi.interval_number == 3

   assert hdi is not mdi
   assert not hdi == mdi
