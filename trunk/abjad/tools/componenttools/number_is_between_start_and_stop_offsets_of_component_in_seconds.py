from abjad.tools import durationtools


def number_is_between_start_and_stop_offsets_of_component_in_seconds(timepoint, component):
    '''.. versionadded:: 2.0

    True when `timepoint` is within the duration of `component` in seconds::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.TempoMark(Duration(1, 2), 60, target_context = Staff)(staff)
        TempoMark(Duration(1, 2), 60)(Staff{4})

    ::

        abjad> leaf = staff.leaves[0]
        abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.1, leaf)
        True
        abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.333, leaf) # doctest: +SKIP
        True

    Otherwise false::

        abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.5, staff) # doctest: +SKIP
        False

    Return boolean.
    '''

    try:
        timepoint = durationtools.Duration(timepoint)
    except TypeError:
        pass

    return component._offset.start_in_seconds <= timepoint < \
        component._offset.stop_in_seconds
