from abjad import *


def test_componenttools_number_is_between_start_and_stop_offsets_of_component_in_seconds_01():
    '''True when split point is within duration of component, in seconds.'''

    staff = Staff([Note("c'4")])
    t = staff[0]
    contexttools.TempoMark(Duration(1, 2), 60, target_context = Staff)(staff)

    assert componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0, t)
    assert componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.1, t)
    assert componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.333, t)
    assert not componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(
        0.5, t)
