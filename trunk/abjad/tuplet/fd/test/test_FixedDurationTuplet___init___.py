from abjad import *


def test_fdtuplet_init_01( ):
   '''Initialize typical fixed-duration tuplet.'''
   
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)

   assert repr(t) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
   assert str(t) == "{@ 3:2 c'8, c'8, c'8 @}"
   assert t.format == "\\times 2/3 {\n\tc'8\n\tc'8\n\tc'8\n}"
   assert len(t) == 3
   assert t.duration.target == Rational(1, 4)
   assert t.duration.multiplier == Rational(2, 3)
   assert t.duration.prolated == Rational(1, 4)


def test_fdtuplet_init_02( ):
   '''Initialize empty fixed-duration tuplet.'''

   t = FixedDurationTuplet((1, 4), [ ])

   assert repr(t) == 'FixedDurationTuplet(1/4, [ ])'
   assert str(t) == '{@ 1/4 @}'
   assert len(t) == 0
   assert t.duration.target == Rational(1, 4)
   assert t.duration.multiplier == None
   assert t.duration.prolated == Rational(1, 4)
