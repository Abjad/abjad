from abjad import *


def test_NamedPitch_diatonic_pitch_class_number_01( ):

   assert pitchtools.NamedPitch("c''").diatonic_pitch_class_number == 0
   assert pitchtools.NamedPitch("cs''").diatonic_pitch_class_number == 0
   assert pitchtools.NamedPitch("d''").diatonic_pitch_class_number == 1
   assert pitchtools.NamedPitch("ef''").diatonic_pitch_class_number == 2
   assert pitchtools.NamedPitch("e''").diatonic_pitch_class_number == 2
   assert pitchtools.NamedPitch("f''").diatonic_pitch_class_number == 3
   assert pitchtools.NamedPitch("fs''").diatonic_pitch_class_number == 3
   assert pitchtools.NamedPitch("g''").diatonic_pitch_class_number == 4
   assert pitchtools.NamedPitch("af''").diatonic_pitch_class_number == 5
   assert pitchtools.NamedPitch("a''").diatonic_pitch_class_number == 5
   assert pitchtools.NamedPitch("bf''").diatonic_pitch_class_number == 6
   assert pitchtools.NamedPitch("b''").diatonic_pitch_class_number == 6
