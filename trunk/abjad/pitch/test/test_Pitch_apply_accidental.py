from abjad import *


def test_Pitch_apply_accidental_01( ):

   assert Pitch('cs', 4).apply_accidental('sharp') == Pitch('css', 4)
   assert Pitch('cs', 4).apply_accidental('flat') == Pitch('c', 4)
   assert Pitch('cs', 4).apply_accidental('natural') == Pitch('cs', 4)
   assert Pitch('cs', 4).apply_accidental('quarter sharp') == Pitch('ctqs', 4)
