from abjad import *


def test_Pitch___add___01( ):

   pitch = Pitch(12)
   diatonic_interval = pitchtools.DiatonicInterval('minor', 2)

   assert pitch + diatonic_interval == Pitch('df', 5)


def test_Pitch___add___02( ):

   pitch = Pitch(12)
   chromatic_interval = pitchtools.ChromaticInterval(1)

   assert pitch + chromatic_interval == Pitch('cs', 5)
