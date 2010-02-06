from abjad import *


def test_MelodicDiatonicIntervalSet_harmonic_diatonic_interval_set_01( ):

   mdiset = pitchtools.MelodicDiatonicIntervalSet([ ])
   mdiset.add(pitchtools.MelodicDiatonicInterval('minor', -2))
   mdiset.add(pitchtools.MelodicDiatonicInterval('major', -2))
   mdiset.add(pitchtools.MelodicDiatonicInterval('minor', 2))
   mdiset.add(pitchtools.MelodicDiatonicInterval('major', 2))
   "MelodicDiatonicIntervalSet(-m2, -M2, +M2, +m2)"

   derived_hdiset = mdiset.harmonic_diatonic_interval_set
   manual_hdiset = pitchtools.HarmonicDiatonicIntervalSet([ ])
   manual_hdiset.add(pitchtools.HarmonicDiatonicInterval('minor', 2))
   manual_hdiset.add(pitchtools.HarmonicDiatonicInterval('major', 2))

   assert derived_hdiset == manual_hdiset
