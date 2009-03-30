from abjad import *


def test_notehead_grob_handling_01( ):
   '''Abjad NoteHead handles LilyPond NoteHead grob.'''

   t = Note(13, (1, 4))
   t.notehead.transparent = True

   assert t.notehead.transparent
   assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"

   t.notehead.transparent = None
   assert t.format == "cs''4"
