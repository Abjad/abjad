from abjad import *


def test_ChromaticIntervalVector_has_none_of_01( ):

   civ = pitchtools.ChromaticIntervalVector(Staff(macros.scale(5)))

   "0 1 3 2 1 2 0 1 0 0 0 0"

   assert not civ.has_none_of([0, 1, 2])
   assert not civ.has_none_of([3, 4, 5])
   assert not civ.has_none_of([6, 7, 8])
   assert civ.has_none_of([9, 10, 11])
