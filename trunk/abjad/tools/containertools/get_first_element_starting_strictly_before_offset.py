from abjad.tools import durationtools


def get_first_element_starting_strictly_before_offset(container, prolated_offset):
    '''.. versionadded:: 2.0

    Get first `container` element starting strictly before `prolated_offset`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> containertools.get_first_element_starting_strictly_before_offset(staff, Duration(1, 8))
        Note("c'8")

    Return component.

    Return none when `container` element starts stirctly before `prolated_offset`.
    '''

    prolated_offset = durationtools.Duration(prolated_offset)

    for element in reversed(container):
        if element.timespan.start_offset < prolated_offset:
            return element
