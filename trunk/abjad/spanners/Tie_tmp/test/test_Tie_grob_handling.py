from abjad import *


def test_Tie_grob_handling_01( ):
   '''
   The Abjad Tie spanner handles the LilyPond Tie grob.
   '''

   t = Voice(leaftools.make_repeated_notes(4))
   p = Tie(t[ : ])
   p.thickness = 3

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
