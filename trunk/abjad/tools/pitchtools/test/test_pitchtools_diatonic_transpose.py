from abjad import *


def test_pitchtools_diatonic_transpose_01( ):

   pitch = Pitch('c', 4)

   interval = pitchtools.DiatonicInterval('perfect', 1)
   transposed_pitch = pitchtools.diatonic_transpose(pitch, interval)
   transposed_pitch == Pitch('c', 4)

   interval = pitchtools.DiatonicInterval('minor', 2)
   transposed_pitch = pitchtools.diatonic_transpose(pitch, interval)
   transposed_pitch == Pitch('df', 4)
   
   interval = pitchtools.DiatonicInterval('major', 2)
   transposed_pitch = pitchtools.diatonic_transpose(pitch, interval)
   transposed_pitch == Pitch('d', 4)
   
   interval = pitchtools.DiatonicInterval('minor', 3)
   transposed_pitch = pitchtools.diatonic_transpose(pitch, interval)
   transposed_pitch == Pitch('ef', 4)
   
   interval = pitchtools.DiatonicInterval('major', 3)
   transposed_pitch = pitchtools.diatonic_transpose(pitch, interval)
   transposed_pitch == Pitch('e', 4)
