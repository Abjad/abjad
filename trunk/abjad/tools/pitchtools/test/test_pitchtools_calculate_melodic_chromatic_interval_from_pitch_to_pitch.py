from abjad import *


def test_pitchtools_calculate_melodic_chromatic_interval_from_pitch_to_pitch_01( ):

   pitch_1 = pitchtools.NamedPitch(10)
   pitch_2 = pitchtools.NamedPitch(12)

   mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
      pitch_1, pitch_2)
   assert mci == pitchtools.MelodicChromaticInterval(2)

   mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
      pitch_2, pitch_1)
   assert mci == pitchtools.MelodicChromaticInterval(-2)

   mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
      pitch_1, pitch_1)
   assert mci == pitchtools.MelodicChromaticInterval(0)

   mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
      pitch_2, pitch_2)
   assert mci == pitchtools.MelodicChromaticInterval(0)


def test_pitchtools_calculate_melodic_chromatic_interval_from_pitch_to_pitch_02( ):
   '''Works with quartertones.'''

   mci = pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9.5)) 
   assert mci == pitchtools.MelodicChromaticInterval(-2.5)
