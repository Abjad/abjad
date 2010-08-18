from abjad import *


def test_FixedDurationTuplet_trivial_01( ):
   '''True when tuplet ratio equals one.'''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   assert not t.trivial


def test_FixedDurationTuplet_trivial_02( ):
   '''True when tuplet ratio equals one.'''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(2))
   assert t.trivial
