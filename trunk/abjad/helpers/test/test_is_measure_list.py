from abjad.helpers.is_measure_list import _is_measure_list
from abjad import *


def test_is_measure_list_01( ):
   '''True on list of orphan measures.'''

   t = RigidMeasure((3, 8), scale(3)) * 3
   assert _is_measure_list(t)


def test_is_measure_list_02( ):
   '''True on list of containerized measures.'''

   measures = RigidMeasure((3, 8), scale(3)) * 3
   t = Staff(measures)
   assert _is_measure_list(t[:])


def test_is_measure_list_03( ):
   '''False on lone measure.'''

   assert not _is_measure_list(RigidMeasure((3, 8), scale(3)))


def test_is_measure_list_04( ):
   '''True on empty list.'''

   assert _is_measure_list([ ])
