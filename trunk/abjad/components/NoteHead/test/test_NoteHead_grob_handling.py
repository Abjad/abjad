from abjad import *


def test_NoteHead_grob_handling_01( ):
   '''Abjad NoteHead handles LilyPond NoteHead grob.'''

   t = Note(13, (1, 4))
   t.note_head.transparent = True

   assert t.note_head.transparent
   assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"

   t.note_head.transparent = None
   assert t.format == "cs''4"


def test_NoteHead_grob_handling_02( ):
   '''From a bug fix. Pitch should never show up as a grob
   override because pitch is a fully managed note head attribute.'''

   t = Rest((1, 8))
   note = Note(t)
   note.pitch = 2

   assert note.format == "d'8"

   note.note_head.color = 'red'
   
   assert note.format == "\\once \\override NoteHead #'color = #red\nd'8"
