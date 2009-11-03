from abjad import *


def test_note_head_init_01( ):

   t = NoteHead(None, 6)
   new = NoteHead(None, t)

   assert t is not new
   assert t.pitch.number == 6
   assert new.pitch.number == 6
