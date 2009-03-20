from abjad import *


def test_spanner_begin_01( ):
   '''Return start time of spanner in score.'''

   t = Voice(scale(4))
   beam = Beam(t[1:3])
   glissando = Glissando([t])

   assert beam.begin == Rational(1, 8)
   assert glissando.begin == Rational(0)
