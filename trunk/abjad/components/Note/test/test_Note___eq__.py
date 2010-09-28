from abjad import *


def test_Note___eq___01( ):

   note_1 = Note(0, (1, 4))
   note_2 = Note(0, (1, 4))
   note_3 = Note(2, (1, 4))

   assert     note_1 == note_2
   assert not note_1 == note_3
   assert not note_2 == note_3
