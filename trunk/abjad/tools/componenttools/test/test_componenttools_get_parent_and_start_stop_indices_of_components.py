from abjad import *


def test_componenttools_get_parent_and_start_stop_indices_of_components_01( ):
   t = Staff(macros.scale(4))
   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(t[2:])
   assert parent is t
   assert start == 2
   assert stop == 3


def test_componenttools_get_parent_and_start_stop_indices_of_components_02( ):
   t = Staff(macros.scale(4))
   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(t[:2])
   assert parent is t
   assert start == 0
   assert stop == 1


def test_componenttools_get_parent_and_start_stop_indices_of_components_03( ):
   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([ ])
   assert parent is None
   assert start is None
   assert stop is None

