from abjad import *


def test_get_parent_and_indices_01( ):
   t = Staff(scale(4))
   parent, start, stop = get_parent_and_indices(t[2:])
   assert parent is t
   assert start == 2
   assert stop == 3


def test_get_parent_and_indices_02( ):
   t = Staff(scale(4))
   parent, start, stop = get_parent_and_indices(t[:2])
   assert parent is t
   assert start == 0
   assert stop == 1


def test_get_parent_and_indices_03( ):
   parent, start, stop = get_parent_and_indices([ ])
   assert parent is None
   assert start is None
   assert stop is None

