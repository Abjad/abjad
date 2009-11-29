from abjad import *


def test_HarmonicChromaticInterval___init___01( ):
   '''Init from positive number.'''

   i = pitchtools.HarmonicChromaticInterval(3)
   assert i.interval_number == 3


def test_HarmonicChromaticInterval___init___02( ):
   '''Init from negative number.'''

   i = pitchtools.HarmonicChromaticInterval(-3)
   assert i.interval_number == 3


def test_HarmonicChromaticInterval___init___03( ):
   '''Init from other harmonic chromatic interval.'''

   i = pitchtools.HarmonicChromaticInterval(3)
   j = pitchtools.HarmonicChromaticInterval(i)
   assert i.interval_number == j.interval_number == 3
   assert i is not j
   

def test_HarmonicChromaticInterval___init___04( ):
   '''Init from melodic diatonic interval.'''

   diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 4)
   i = pitchtools.HarmonicChromaticInterval(diatonic_interval)
   assert i.interval_number == 5
