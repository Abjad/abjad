from abjad.tools import durationtools


def number_is_between_start_and_stop_offsets_of_component(timepoint, component):
    '''.. versionadded:: 2.0

    True when `timepoint` is within the prolated duration of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> leaf = staff.leaves[0]

    ::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Duration(1, 16), leaf)
        True
    
    ::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Duration(1, 12), leaf)
        True

    Otherwise false::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Duration(1, 4), leaf)
        False

    Return boolean.
    '''

    try:
        timepoint = durationtools.Duration(timepoint)
    except TypeError:
        pass

    return component.start_offset <= timepoint < component.stop_offset
