from abjad import *


def test_componenttools_number_is_between_prolated_start_and_stop_offsets_of_component_01():
    '''True when split point is within prolated duration of component.'''

    assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(0), Note("c'4"))
    assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 16), Note("c'4"))
    assert componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 12), Note("c'4"))
    assert not componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Duration(1, 4), Note("c'4"))
