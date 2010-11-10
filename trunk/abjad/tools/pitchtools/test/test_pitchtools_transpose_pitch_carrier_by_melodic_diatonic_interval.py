from abjad import *


def test_pitchtools_transpose_pitch_carrier_by_melodic_diatonic_interval_01( ):

   pitch = pitchtools.NamedChromaticPitch(12)
   mdi = pitchtools.MelodicDiatonicInterval('minor', -3)

   transposed_pitch = pitchtools.transpose_pitch_carrier_by_melodic_diatonic_interval(pitch, mdi) 
   assert transposed_pitch == pitchtools.NamedChromaticPitch('a', 4)
