from abjad import *
import py


def test_NoteHead_grob_handling_01( ):
   '''Abjad NoteHead handles LilyPond NoteHead grob.'''

   t = Note(13, (1, 4))
   t.override.note_head.transparent = True

   assert t.override.note_head.transparent
   assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"

   del(t.override.note_head.transparent)
   assert t.format == "cs''4"


def test_NoteHead_grob_handling_02( ):
   '''From a bug fix. Pitch should never show up as a grob
   override because pitch is a fully managed note head attribute.'''
   py.test.skip('fix broken reg test having to do with note head.')

   t = Rest((1, 8))
   note = Note(t)
   note.pitch = 2

   assert note.format == "d'8"

   note.override.note_head.color = 'red'
   
   assert note.format == "\\once \\override NoteHead #'color = #red\nd'8"
