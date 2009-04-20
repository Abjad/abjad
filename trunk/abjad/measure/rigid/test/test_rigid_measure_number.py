from abjad import *


def test_rigid_measure_number_01( ):
   '''Measures in staff number correctly starting from 1.'''

   t = Staff(measuretools.make([(3, 16), (5, 16), (5, 16)]))
   assert t[0].number == 1
   assert t[1].number == 2
   assert t[2].number == 3


def test_rigid_measure_number_02( ):
   '''Orphan measures number correctly starting from 1.'''

   t = RigidMeasure((3, 8), construct.scale(3))
   assert t.number == 1
