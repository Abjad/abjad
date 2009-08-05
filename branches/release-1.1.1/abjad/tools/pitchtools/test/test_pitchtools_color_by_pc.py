from abjad import *


def test_pitchtools_color_by_pc_01( ):

   t = Note(12, (1, 4))
   pitchtools.color_by_pc(t)

   r'''
   \once \override NoteHead #'color = #(x11-color 'red)
   c''4
   '''

   assert check.wf(t)
   assert t.format == "\\once \\override NoteHead #'color = #(x11-color 'red)\nc''4"
