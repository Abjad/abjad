from abjad import *


def test_note_column_interface_grob_handling_01( ):

   t = Note(0, (1, 4))
   t.note_column.ignore_collision = True

   r'''
   \once \override NoteColumn #'ignore-collision = ##t
   c'4
   '''

   assert check.wf(t)
   assert t.format == "\\once \\override NoteColumn #'ignore-collision = ##t\nc'4"


def test_note_column_interface_grob_handling_02( ):

   t = Staff(construct.scale(4))
   t.note_column.ignore_collision = True

   r'''\new Staff \with {
      \override NoteColumn #'ignore-collision = ##t
   } {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff \\with {\n\t\\override NoteColumn #'ignore-collision = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
