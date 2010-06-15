from abjad import *


def test_componenttools_number_is_between_prolated_start_and_stop_offsets_of_component_01( ):
   '''True when split point is within prolated duration of component.'''

   assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(0), Note(0, (1, 4)))
   assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 16), Note(0, (1, 4)))
   assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 12), Note(0, (1, 4)))
   assert not componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 4), Note(0, (1, 4)))
