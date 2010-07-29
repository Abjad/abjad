from abjad import *


def test_tempo_spanner_grob_handling_01( ):
   '''The Abjad Tempo spanner handles the LilyPond MetronomeMark grob.
   Note context promotion.
   '''

   t = Voice(macros.scale(4))
   p = TempoSpanner(t[:], tempotools.TempoIndication(Rational(1, 4), 58))
   p.color = 'red'
   overridetools.promote_attribute_to_context_on_grob_handler(p, 'color', 'Staff')
   
   r'''
   \new Voice {
      \override Staff.MetronomeMark #'color = #red
      \tempo 4=58
      c'8
      d'8
      e'8
      f'8
      \revert Staff.MetronomeMark #'color
      %% tempo 4=58 ends here
   }
   '''

   assert t.format == "\\new Voice {\n\t\\override Staff.MetronomeMark #'color = #red\n\t\\tempo 4=58\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.MetronomeMark #'color\n\t%% tempo 4=58 ends here\n}"
