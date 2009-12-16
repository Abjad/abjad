from abjad import *


def test_containertools_get_first_element_starting_not_before_prolated_offset_01( ):
   
   staff = Staff(construct.scale(8))
   t = containertools.get_first_element_starting_not_before_prolated_offset(
      staff, Rational(5, 32))

   assert t is staff[2]


def test_containertools_get_first_element_starting_not_before_prolated_offset_02( ):
   '''No element boundary case.'''
   
   staff = Staff(construct.scale(8))
   t = containertools.get_first_element_starting_not_before_prolated_offset(
      staff, Rational(15, 8))

   assert t is None
