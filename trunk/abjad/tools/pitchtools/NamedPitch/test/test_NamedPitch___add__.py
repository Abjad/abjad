from abjad import *


def test_NamedPitch___add___01( ):

   pitch = pitchtools.NamedPitch(12)
   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)

   assert pitch + diatonic_interval == pitchtools.NamedPitch('df', 5)


def test_NamedPitch___add___02( ):

   pitch = pitchtools.NamedPitch(12)
   chromatic_interval = pitchtools.MelodicChromaticInterval(1)

   assert pitch + chromatic_interval == pitchtools.NamedPitch('cs', 5)
