from abjad import *


def test_numbering_measures_01( ):
   '''Measures in staff number correctly starting from 1.'''

   t = Staff(measuretools.make([(3, 16), (5, 16), (5, 16)]))
   assert t[0].numbering.measure == 1
   assert t[1].numbering.measure == 2
   assert t[2].numbering.measure == 3


def test_numbering_measures_02( ):
   '''Orphan measures number correctly starting from 1.'''

   t = RigidMeasure((3, 8), construct.scale(3))
   assert t.numbering.measure == 1
