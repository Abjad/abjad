from abjad import *


def test_HarmonicChromaticInterval_interval_class_01( ):

   assert pitchtools.HarmonicChromaticInterval(2).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(14).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(26).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(38).interval_class == 2


def test_HarmonicChromaticInterval_interval_class_02( ):

   assert pitchtools.HarmonicChromaticInterval(-2).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(-14).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(-26).interval_class == 2
   assert pitchtools.HarmonicChromaticInterval(-38).interval_class == 2
