from abjad import *


def test_Note___ne___01( ):

   note_1 = Note(0, (1, 4))
   note_2 = Note(0, (1, 4))
   note_3 = Note(2, (1, 4))

   assert not note_1 != note_2
   assert     note_1 != note_3
   assert     note_2 != note_3
