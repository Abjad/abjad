from abjad import *


def test__SpanerDurationInterface_written_01( ):
   t = Voice([RigidMeasure((2, 12), macros.scale(2)), 
      RigidMeasure((2, 8), macros.scale(2))])
   beam = BeamSpanner(t.leaves)
   crescendo = CrescendoSpanner(t[0][:])
   decrescendo = DecrescendoSpanner(t[1][:])

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

   assert beam.duration.written == Rational(4, 8)
   assert crescendo.duration.written == Rational(2, 8)
   assert decrescendo.duration.written == Rational(2, 8)
