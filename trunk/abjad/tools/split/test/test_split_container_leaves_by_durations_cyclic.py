from abjad import *


def test_split_container_leaves_by_durations_cyclic_01( ):
   '''Split leaves contained at any level of depth in container.
      Take split points cyclically from Python durations list.
      Do not fracture spanners.'''

   t = Voice(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''\new Voice {
         \time 2/8
         c'8 [
         d'8
         \time 2/8
         e'8
         f'8 ]
   }'''

   split.container_leaves_by_durations_cyclic(t, [(1, 16)])

   r'''\new Voice {
         \time 2/8
         c'16 [ ~
         c'16
         d'16 ~
         d'16
         \time 2/8
         e'16 ~
         e'16
         f'16 ~
         f'16 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'16 [ ~\n\t\tc'16\n\t\td'16 ~\n\t\td'16\n\t\t\\time 2/8\n\t\te'16 ~\n\t\te'16\n\t\tf'16 ~\n\t\tf'16 ]\n}"


def test_split_container_leaves_by_durations_cyclic_02( ):
   '''Split leaves contained at any level of depth in container.
      Take split points cyclically from Python durations list.'''

   t = Voice(Note(0, (3, 8)) * 4)
   pitchtools.diatonicize(t)

   split.container_leaves_by_durations_cyclic(t, [(1, 4)])

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
