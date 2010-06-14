from abjad import *


def test_fdtuplet_trivial_01( ):
   '''True when tuplet ratio equals one.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   assert not t.trivial


def test_fdtuplet_trivial_02( ):
   '''True when tuplet ratio equals one.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   assert t.trivial
