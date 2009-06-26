from abjad import *


def test_notehead_grob_handling_01( ):
   '''Abjad NoteHead handles LilyPond NoteHead grob.'''

   t = Note(13, (1, 4))
   t.notehead.transparent = True

   assert t.notehead.transparent
   assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"

   t.notehead.transparent = None
   assert t.format == "cs''4"


def test_notehead_grob_handling_02( ):
   '''From a bug fix. Pitch should never show up as a grob
   override because pitch is a fully managed note head attribute.'''

   t = Rest((1, 8))
   note = Note(t)
   note.pitch = 2

   assert note.format == "d'8"

   note.notehead.color = 'red'
   
   assert note.format == "\\once \\override NoteHead #'color = #red\nd'8"
