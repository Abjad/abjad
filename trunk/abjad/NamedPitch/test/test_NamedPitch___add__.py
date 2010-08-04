from abjad import *


def test_NamedPitch___add___01( ):

   pitch = NamedPitch(12)
   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)

   assert pitch + diatonic_interval == NamedPitch('df', 5)


def test_NamedPitch___add___02( ):

   pitch = NamedPitch(12)
   chromatic_interval = pitchtools.MelodicChromaticInterval(1)

   assert pitch + chromatic_interval == NamedPitch('cs', 5)
