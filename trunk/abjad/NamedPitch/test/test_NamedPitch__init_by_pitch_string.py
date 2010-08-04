from abjad import *


def test_NamedPitch__init_by_pitch_string_01( ):
  
   assert NamedPitch("cs'''") == NamedPitch('cs', 6)
   assert NamedPitch("cs''") == NamedPitch('cs', 5)
   assert NamedPitch("cs'") == NamedPitch('cs', 4)
   assert NamedPitch('cs') == NamedPitch('cs', 3)
   assert NamedPitch('cs,') == NamedPitch('cs', 2)
   assert NamedPitch('cs,,') == NamedPitch('cs', 1)
   assert NamedPitch('cs,,,') == NamedPitch('cs', 0)
