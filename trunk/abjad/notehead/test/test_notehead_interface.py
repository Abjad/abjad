from abjad import *


def test_notehead_interface_01( ):
   '''Override LilyPond NoteHead grob on voice.'''

   t = Voice(scale(4))
   t.notehead.color = 'red'

   r'''
   \new Voice \with {
      \override NoteHead #'color = #red
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice \\with {\n\t\\override NoteHead #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
