from abjad import *


def test_SchemeColor___init____01( ):
   '''Init scheme color with string.
   '''

   t = Note(0, (1, 4))
   t.override.note_head.color = schemetools.SchemeColor('ForestGreen')

   r'''
   \once \override NoteHead #'color = #(x11-color 'ForestGreen)
   c'4
   '''

   assert t.format == "\\once \\override NoteHead #'color = #(x11-color 'ForestGreen)\nc'4"


def test_SchemeColor___init____02( ):
   '''Normal (non-X11) color names specify with a string.'''
   
   t = Note(0, (1, 4))
   t.override.note_head.color = 'grey'

   r'''
   \once \override NoteHead #'color = #grey
   c'4
   '''

   assert t.format == "\\once \\override NoteHead #'color = #grey\nc'4"
