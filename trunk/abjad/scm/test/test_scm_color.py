from abjad import *


def test_scm_color_01( ):

   t = Note(0, (1, 4))
   t.note_head.color = Color('ForestGreen')
   assert t.format == "\\once \\override NoteHead #'color = #(x11-color 'ForestGreen)\nc'4"


def test_scm_color_02( ):
   '''Normal (non-X11) color names specify with a string.'''
   
   t = Note(0, (1, 4))
   t.note_head.color = 'grey'

   r'''
   \once \override NoteHead #'color = #grey
   c'4
   '''

   assert t.format == "\\once \\override NoteHead #'color = #grey\nc'4"
