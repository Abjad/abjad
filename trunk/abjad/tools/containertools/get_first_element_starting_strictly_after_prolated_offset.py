from abjad.tools import durationtools


def get_first_element_starting_strictly_after_prolated_offset(container, prolated_offset):
    '''.. versionadded:: 2.0

    Get first `container` element starting strictly after `prolated_offset`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> containertools.get_first_element_starting_strictly_after_prolated_offset(staff, Duration(1, 8))
        Note("e'8")

    Return component.

    Return none when no `container` element starts strictly after `prolated_offset`.

    .. versionchanged:: 2.0
        renamed ``containertools.get_leftmost_element_starting_after_prolated_offset()`` to
        ``containertools.get_first_element_starting_strictly_after_prolated_offset()``.
    '''

    prolated_offset = durationtools.Duration(prolated_offset)

    for element in container:
        if prolated_offset < element._offset.start:
            return element
