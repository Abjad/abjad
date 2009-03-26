from abjad import *


def test_get_parent_and_index_01( ):
   t = Staff(scale(4))
   parent, index = get_parent_and_index(t[2:])
   assert parent is t
   assert index == 2


def test_get_parent_and_index_02( ):
   t = Staff(scale(4))
   parent, index = get_parent_and_index(t[:2])
   assert parent is t
   assert index == 0


def test_get_parent_and_index_03( ):
   parent, index = get_parent_and_index([ ])
   assert parent is None
   assert index is None

