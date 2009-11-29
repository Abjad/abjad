from abjad import *


def test_MelodicChromaticInterval_interval_class_01( ):

   assert pitchtools.MelodicChromaticInterval(2).interval_class == 2
   assert pitchtools.MelodicChromaticInterval(14).interval_class == 2
   assert pitchtools.MelodicChromaticInterval(26).interval_class == 2
   assert pitchtools.MelodicChromaticInterval(38).interval_class == 2


def test_MelodicChromaticInterval_interval_class_02( ):

   assert pitchtools.MelodicChromaticInterval(-2).interval_class == -2
   assert pitchtools.MelodicChromaticInterval(-14).interval_class == -2
   assert pitchtools.MelodicChromaticInterval(-26).interval_class == -2
   assert pitchtools.MelodicChromaticInterval(-38).interval_class == -2
