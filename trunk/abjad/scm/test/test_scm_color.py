from abjad import *


def test_scm_color_01( ):

   t = Note(0, (1, 4))
   t.note_head.color = Color('ForestGreen')
   assert t.format == "\\once \\override NoteHead #'color = #(x11-color 'ForestGreen)\nc'4"
