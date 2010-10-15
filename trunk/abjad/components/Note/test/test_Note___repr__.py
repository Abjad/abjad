from abjad import *


def test_Note___repr___01( ):
   '''Note repr is evaluable.
   '''

   note_1 = Note(0, (1, 4))
   note_2 = eval(repr(note_1))

   assert isinstance(note_1, Note)
   assert isinstance(note_2, Note)
   assert note_1 == note_2
   assert note_1 is not note_2
