from abjad import *


def test_parenttools_get_with_indices_01( ):
   t = Staff(construct.scale(4))
   parent, start, stop = parenttools.get_with_indices(t[2:])
   assert parent is t
   assert start == 2
   assert stop == 3


def test_parenttools_get_with_indices_02( ):
   t = Staff(construct.scale(4))
   parent, start, stop = parenttools.get_with_indices(t[:2])
   assert parent is t
   assert start == 0
   assert stop == 1


def test_parenttools_get_with_indices_03( ):
   parent, start, stop = parenttools.get_with_indices([ ])
   assert parent is None
   assert start is None
   assert stop is None

