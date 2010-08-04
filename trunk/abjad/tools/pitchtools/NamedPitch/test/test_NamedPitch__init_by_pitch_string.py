from abjad import *


def test_NamedPitch__init_by_pitch_string_01( ):
  
   assert pitchtools.NamedPitch("cs'''") == pitchtools.NamedPitch('cs', 6)
   assert pitchtools.NamedPitch("cs''") == pitchtools.NamedPitch('cs', 5)
   assert pitchtools.NamedPitch("cs'") == pitchtools.NamedPitch('cs', 4)
   assert pitchtools.NamedPitch('cs') == pitchtools.NamedPitch('cs', 3)
   assert pitchtools.NamedPitch('cs,') == pitchtools.NamedPitch('cs', 2)
   assert pitchtools.NamedPitch('cs,,') == pitchtools.NamedPitch('cs', 1)
   assert pitchtools.NamedPitch('cs,,,') == pitchtools.NamedPitch('cs', 0)
