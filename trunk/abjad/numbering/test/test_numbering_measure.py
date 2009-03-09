from abjad import *


def test_numbering_measures_01( ):
   '''Measures in staff number correctly.'''

   t = Staff(measures_make([(3, 16), (5, 16), (5, 16)]))
   assert t[0].numbering.measure == 0
   assert t[1].numbering.measure == 1
   assert t[2].numbering.measure == 2


def test_numbering_measures_02( ):
   '''Orphan measures number correctly.'''

   t = RigidMeasure((3, 8), scale(3))
   assert t.numbering.measure == 0
