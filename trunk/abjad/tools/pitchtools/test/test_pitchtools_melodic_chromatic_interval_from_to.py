from abjad import *


def test_pitchtools_melodic_chromatic_interval_from_to_01( ):

   pitch_1 = Pitch(10)
   pitch_2 = Pitch(12)

   mci = pitchtools.melodic_chromatic_interval_from_to(
      pitch_1, pitch_2)
   assert mci == pitchtools.MelodicChromaticInterval(2)

   mci = pitchtools.melodic_chromatic_interval_from_to(
      pitch_2, pitch_1)
   assert mci == pitchtools.MelodicChromaticInterval(-2)

   mci = pitchtools.melodic_chromatic_interval_from_to(
      pitch_1, pitch_1)
   assert mci == pitchtools.MelodicChromaticInterval(0)

   mci = pitchtools.melodic_chromatic_interval_from_to(
      pitch_2, pitch_2)
   assert mci == pitchtools.MelodicChromaticInterval(0)


def test_pitchtools_melodic_chromatic_interval_from_to_02( ):
   '''Works with quartertones.'''

   mci = pitchtools.melodic_chromatic_interval_from_to(
      Pitch(12), Pitch(9.5)) 
   assert mci == pitchtools.MelodicChromaticInterval(-2.5)
