from abjad import *


def test_containertools_get_first_element_starting_before_or_at_prolated_offset_01( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Rational(1, 8))

   assert element is staff[1]



def test_containertools_get_first_element_starting_before_or_at_prolated_offset_02( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Rational(3, 16))

   assert element is staff[1]


def test_containertools_get_first_element_starting_before_or_at_prolated_offset_03( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_before_or_at_prolated_offset(staff, 99)

   assert element is staff[-1]


def test_containertools_get_first_element_starting_before_or_at_prolated_offset_04( ):
   '''Return none when no element in container starts not after
   prolated offset.'''

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Rational(-1, 8))

   assert element is None
