from abjad.tools import durationtools


def get_first_element_starting_at_or_after_offset(container, prolated_offset):
    '''.. versionadded:: 2.0

    Get first `container` element starting at or after `prolated_offset`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> containertools.get_first_element_starting_at_or_after_offset(staff, Duration(1, 8))
        Note("d'8")

    Return component.

    Return none when no `container` element starts at or after `prolated_offset`.

    .. versionchanged:: 2.0
        renamed ``containertools.get_leftmost_element_starting_not_before_prolated_offset()`` to
        ``containertools.get_first_element_starting_at_or_after_offset()``.
    '''

    prolated_offset = durationtools.Duration(prolated_offset)

    for element in container:
        if prolated_offset <= element.start_offset:
            return element
