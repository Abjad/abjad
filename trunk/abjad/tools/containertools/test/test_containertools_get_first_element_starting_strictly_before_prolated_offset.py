from abjad import *


def test_containertools_get_first_element_starting_strictly_before_prolated_offset_01( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_strictly_before_prolated_offset(staff, Duration(1, 8))

   assert element is staff[0]



def test_containertools_get_first_element_starting_strictly_before_prolated_offset_02( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_strictly_before_prolated_offset(staff, Duration(3, 16))

   assert element is staff[1]


def test_containertools_get_first_element_starting_strictly_before_prolated_offset_03( ):

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_strictly_before_prolated_offset(staff, 99)

   assert element is staff[-1]


def test_containertools_get_first_element_starting_strictly_before_prolated_offset_04( ):
   '''Return none when no element in container starts before
   prolated offset.'''

   staff = Staff(macros.scale(4))
   element = containertools.get_first_element_starting_strictly_before_prolated_offset(staff, Duration(0))

   assert element is None
