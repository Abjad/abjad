from abjad import *


def test_metric_slice_01( ):
   '''Slice leaves in voice according to metric grid.'''

   t = Voice(Note(0, (3, 8)) * 4)
   pitchtools.diatonicize(t)

   metric_slice(t, [(1, 4)])

   r'''\new Voice {
      c'4 ~
      c'8
      d'8 ~
      d'4
      e'4 ~
      e'8
      f'8 ~
      f'4
   }'''

   assert check.wf(t)
   assert len(t) == 8
   assert len(t.spanners.attached) == 0
   assert t[0].duration.prolated == Rational(1, 4)
   assert t[1].duration.prolated == Rational(1, 8)
   assert t[0].tie.spanner is t[1].tie.spanner
   assert t[2].duration.prolated == Rational(1, 8)
   assert t[3].duration.prolated == Rational(1, 4)
   assert t[2].tie.spanner is t[3].tie.spanner
   assert t[4].duration.prolated == Rational(1, 4)
   assert t[5].duration.prolated == Rational(1, 8)
   assert t[4].tie.spanner is t[5].tie.spanner
   assert t[6].duration.prolated == Rational(1, 8)
   assert t[7].duration.prolated == Rational(1, 4)
   assert t[6].tie.spanner is t[7].tie.spanner

   assert t.format == "\\new Voice {\n\tc'4 ~\n\tc'8\n\td'8 ~\n\td'4\n\te'4 ~\n\te'8\n\tf'8 ~\n\tf'4\n}"
