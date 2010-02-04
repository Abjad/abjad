from abjad import *


def test_Pitch__init_by_pitch_string_01( ):
  
   assert Pitch("cs'''") == Pitch('cs', 7)
   assert Pitch("cs''") == Pitch('cs', 6)
   assert Pitch("cs'") == Pitch('cs', 5)
   assert Pitch('cs') == Pitch('cs', 4)
   assert Pitch('cs,') == Pitch('cs', 3)
   assert Pitch('cs,,') == Pitch('cs', 2)
   assert Pitch('cs,,,') == Pitch('cs', 1)
