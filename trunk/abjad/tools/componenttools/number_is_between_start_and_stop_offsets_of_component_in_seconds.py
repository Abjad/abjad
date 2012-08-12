from abjad.tools import durationtools


def number_is_between_start_and_stop_offsets_of_component_in_seconds(timepoint, component):
    '''.. versionadded:: 2.0

    True when `timepoint` is within the duration of `component` in seconds::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.TempoMark(Duration(1, 4), 60, target_context=Staff)(staff)
        TempoMark(Duration(1, 4), 60)(Staff{4})

    ::

        >>> leaf = staff.leaves[0]

    ::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(
        ... 0.1, leaf)
        True

    Otherwise false::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(
        ... 0.5, leaf)
        False

    Return boolean.
    '''

    try:
        timepoint = durationtools.Offset(timepoint)
    except TypeError:
        pass

    return component.start_offset_in_seconds <= timepoint < component.stop_offset_in_seconds
