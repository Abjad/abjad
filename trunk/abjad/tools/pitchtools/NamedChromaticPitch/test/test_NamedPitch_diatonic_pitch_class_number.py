from abjad import *


def test_NamedPitch_diatonic_pitch_class_number_01( ):

   assert pitchtools.NamedChromaticPitch("c''").diatonic_pitch_class_number == 0
   assert pitchtools.NamedChromaticPitch("cs''").diatonic_pitch_class_number == 0
   assert pitchtools.NamedChromaticPitch("d''").diatonic_pitch_class_number == 1
   assert pitchtools.NamedChromaticPitch("ef''").diatonic_pitch_class_number == 2
   assert pitchtools.NamedChromaticPitch("e''").diatonic_pitch_class_number == 2
   assert pitchtools.NamedChromaticPitch("f''").diatonic_pitch_class_number == 3
   assert pitchtools.NamedChromaticPitch("fs''").diatonic_pitch_class_number == 3
   assert pitchtools.NamedChromaticPitch("g''").diatonic_pitch_class_number == 4
   assert pitchtools.NamedChromaticPitch("af''").diatonic_pitch_class_number == 5
   assert pitchtools.NamedChromaticPitch("a''").diatonic_pitch_class_number == 5
   assert pitchtools.NamedChromaticPitch("bf''").diatonic_pitch_class_number == 6
   assert pitchtools.NamedChromaticPitch("b''").diatonic_pitch_class_number == 6
