from abjad import *


def test__SpannerDurationInterface_prolated_01( ):
   t = Voice([RigidMeasure((2, 12), macros.scale(2)), 
      RigidMeasure((2, 8), macros.scale(2))])
   beam = Beam(t.leaves)
   crescendo = Crescendo(t[0][:])
   decrescendo = Decrescendo(t[1][:])

   r'''
   \new Voice {
                   \time 2/12
                   \scaleDurations #'(2 . 3) {
                           c'8 [ \<
                           d'8 \!
                   }
                   \time 2/8
                   c'8 \>
                   d'8 ] \!
   }
   '''

   assert beam.duration.prolated == Rational(5, 12)
   assert crescendo.duration.prolated == Rational(2, 12)
   assert decrescendo.duration.prolated == Rational(2, 8)
