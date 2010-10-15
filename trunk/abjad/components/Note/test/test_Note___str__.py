from abjad import *


def test_Note___str___01( ):

   note = Note(0, (1, 4))

   assert str(note) == "c'4"
