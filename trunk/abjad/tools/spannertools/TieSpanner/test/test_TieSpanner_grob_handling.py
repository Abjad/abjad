from abjad import *


def test_TieSpanner_grob_handling_01( ):
   '''
   The Abjad Tie spanner handles the LilyPond Tie grob.
   '''

   t = Voice(notetools.make_repeated_notes(4))
   p = spannertools.TieSpanner(t[:])
   #p.thickness = 3
   p.override.tie.thickness = 3

   r'''
   \new Voice {
      \override Tie #'thickness = #3
      c'8 ~
      c'8 ~
      c'8 ~
      c'8
      \revert Tie #'thickness
   }
   '''
 
   assert t.format == "\\new Voice {\n\t\\override Tie #'thickness = #3\n\tc'8 ~\n\tc'8 ~\n\tc'8 ~\n\tc'8\n\t\\revert Tie #'thickness\n}"
