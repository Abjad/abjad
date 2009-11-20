from abjad import *


def test_pitchtools_diatonic_transpose_01( ):

   pitch = Pitch('c', 4)

   transposed_pitch = pitchtools.diatonic_transpose(pitch, 'perfect unison')
   transposed_pitch == Pitch('c', 4)

   transposed_pitch = pitchtools.diatonic_transpose(pitch, 'minor second')
   transposed_pitch == Pitch('df', 4)
   
   transposed_pitch = pitchtools.diatonic_transpose(pitch, 'major second')
   transposed_pitch == Pitch('d', 4)
   
   transposed_pitch = pitchtools.diatonic_transpose(pitch, 'minor third')
   transposed_pitch == Pitch('ef', 4)
   
   transposed_pitch = pitchtools.diatonic_transpose(pitch, 'major third')
   transposed_pitch == Pitch('e', 4)
