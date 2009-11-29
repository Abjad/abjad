from abjad import *


def test_pitchtools_DiatonicInterval_interval_class_01( ):

   diatonic_interval = pitchtools.DiatonicInterval('perfect', 1)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.DiatonicInterval('minor', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('major', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('minor', 3)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.DiatonicInterval('major', 3)
   assert diatonic_interval.interval_class == 3


def test_pitchtools_DiatonicInterval_interval_class_02( ):

   diatonic_interval = pitchtools.DiatonicInterval('perfect', 8)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.DiatonicInterval('minor', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('major', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('minor', 10)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.DiatonicInterval('major', 10)
   assert diatonic_interval.interval_class == 3


def test_pitchtools_DiatonicInterval_interval_class_03( ):

   diatonic_interval = pitchtools.DiatonicInterval('perfect', -8)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.DiatonicInterval('minor', -9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('major', -9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.DiatonicInterval('minor', -10)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.DiatonicInterval('major', -10)
   assert diatonic_interval.interval_class == 3
