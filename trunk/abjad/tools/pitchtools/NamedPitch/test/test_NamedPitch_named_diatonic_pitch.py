from abjad import *


def test_NamedPitch_named_diatonic_pitch_01( ):

   assert pitchtools.NamedPitch("cf''").named_diatonic_pitch == \
      pitchtools.NamedDiatonicPitch("c''")

   assert pitchtools.NamedPitch("cqf''").named_diatonic_pitch == \
      pitchtools.NamedDiatonicPitch("c''")

   assert pitchtools.NamedPitch("c''").named_diatonic_pitch == \
      pitchtools.NamedDiatonicPitch("c''")

   assert pitchtools.NamedPitch("cqs''").named_diatonic_pitch == \
      pitchtools.NamedDiatonicPitch("c''")

   assert pitchtools.NamedPitch("cs''").named_diatonic_pitch == \
      pitchtools.NamedDiatonicPitch("c''")
