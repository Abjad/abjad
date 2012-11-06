from abjad.tools import durationtools


def number_is_between_start_and_stop_offsets_of_component(offset, component):
    '''.. versionadded:: 2.0

    True when `offset` is within the prolated duration of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> leaf = staff.leaves[0]

    ::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Offset(1, 16), leaf)
        True
    
    ::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Offset(1, 12), leaf)
        True

    Otherwise false::

        >>> componenttools.number_is_between_start_and_stop_offsets_of_component(
        ...     Offset(1, 4), leaf)
        False

    Return boolean.
    '''

    try:
        offset = durationtools.Offset(offset)
    except TypeError:
        pass

    return component.start_offset <= offset < component.stop_offset
