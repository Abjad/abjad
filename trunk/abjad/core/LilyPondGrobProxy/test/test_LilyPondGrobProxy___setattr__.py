from abjad import *


def test_LilyPondGrobProxy___setattr___01( ):

   note = Note(0, (1, 4))
   note.override.accidental.color = 'red'
   assert note.override.accidental.color == 'red'
