from abjad import *


def test_pitchtools_transpose_by_interval_01( ):

   pitch = Pitch(12)

   diatonic_interval = pitchtools.DiatonicInterval('minor', 2)
   transposed = pitchtools.transpose_by_interval(pitch, diatonic_interval)

   assert transposed == Pitch('df', 5)


def test_pitchtools_transpose_by_interval_02( ):

   pitch = Pitch(12)

   chromatic_interval = pitchtools.ChromaticInterval(1)
   transposed = pitchtools.transpose_by_interval(pitch, chromatic_interval)

   assert transposed == Pitch('cs', 5)
