from abjad import *


def test_pitchtools_transpose_by_melodic_interval_01( ):

   pitch = Pitch(12)

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)
   transposed = pitchtools.transpose_by_melodic_interval(pitch, diatonic_interval)

   assert transposed == Pitch('df', 5)


def test_pitchtools_transpose_by_melodic_interval_02( ):

   pitch = Pitch(12)

   chromatic_interval = pitchtools.MelodicChromaticInterval(1)
   transposed = pitchtools.transpose_by_melodic_interval(pitch, chromatic_interval)

   assert transposed == Pitch('cs', 5)
