from abjad import *


def test_spanner_end_01( ):
   '''Return start time of spanner in score.'''

   t = Voice(scale(4))
   beam = Beam(t[1:3])
   glissando = Glissando([t])

   assert beam.end == Rational(3, 8)
   assert glissando.end == Rational(4, 8)
