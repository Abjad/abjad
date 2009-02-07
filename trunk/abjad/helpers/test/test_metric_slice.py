from abjad import *

def test_metric_slice_01( ):
   t = Voice(Note(0, (3, 8)) * 4)
   metric_slice(t, [(1, 4)])
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
   assert t.format == "\\new Voice {\n\tc'4 ~\n\tc'8\n\tc'8 ~\n\tc'4\n\tc'4 ~\n\tc'8\n\tc'8 ~\n\tc'4\n}"
   r'''
  \new Voice {
        c'4 ~
        c'8
        c'8 ~
        c'4
        c'4 ~
        c'8
        c'8 ~
        c'4
   }
   ''' 
   
