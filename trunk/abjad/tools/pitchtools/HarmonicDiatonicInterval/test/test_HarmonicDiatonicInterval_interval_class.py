from abjad import *


def test_HarmonicDiatonicInterval_interval_class_01( ):

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('perfect', 1)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', 3)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', 3)
   assert diatonic_interval.interval_class == 3


def test_HarmonicDiatonicInterval_interval_class_02( ):

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('perfect', 8)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', 10)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', 10)
   assert diatonic_interval.interval_class == 3


def test_HarmonicDiatonicInterval_interval_class_03( ):

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('perfect', -8)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', -9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', -9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('minor', -10)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.HarmonicDiatonicInterval('major', -10)
   assert diatonic_interval.interval_class == 3
