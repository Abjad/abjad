from abjad import *
import py.test


def test_containertools_get_leftmost_index_starting_after_prolated_offset_01( ):
   
   staff = Staff(construct.scale(4))
   t = containertools.get_leftmost_index_starting_after_prolated_offset(
      staff, Rational(1, 8))

   assert t == 2


def test_containertools_get_leftmost_index_starting_after_prolated_offset_02( ):
   
   staff = Staff(construct.scale(4))
   t = containertools.get_leftmost_index_starting_after_prolated_offset(
      staff, Rational(3, 16))

   assert t is 2


def test_containertools_get_leftmost_index_starting_after_prolated_offset_03( ):
   
   staff = Staff(construct.scale(4))
   t = containertools.get_leftmost_index_starting_after_prolated_offset(
      staff, -99)

   assert t is 0


def test_containertools_get_leftmost_index_starting_after_prolated_offset_04( ):
   
   staff = Staff(construct.scale(4))
   assert py.test.raises(IndexError, 'containertools.get_leftmost_index_starting_after_prolated_offset(staff, 99)')
