from abjad import *


def test_trill_spanner_grob_handling_01( ):
   '''
   The Abjad Trill spanner handles the LilyPond TrillSpanner grob.
   '''

   t = Voice(macros.scale(4))
   p = Trill(t[ : ])
   p.color = 'red'   

   r'''
   \new Voice {
      \override TrillSpanner #'color = #red
      c'8 \startTrillSpan
      d'8
      e'8
      f'8 \stopTrillSpan
      \revert TrillSpanner #'color
   }
   '''

   assert t.format == "\\new Voice {\n\t\\override TrillSpanner #'color = #red\n\tc'8 \\startTrillSpan\n\td'8\n\te'8\n\tf'8 \\stopTrillSpan\n\t\\revert TrillSpanner #'color\n}"
