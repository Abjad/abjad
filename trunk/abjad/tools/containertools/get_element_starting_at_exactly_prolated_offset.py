def get_element_starting_at_exactly_prolated_offset(container, prolated_offset):
    '''.. versionadded:: 2.0

    Get `container` element starting at exactly `prolated_offset`::

        abjad> voice = Voice("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    ::

        abjad> containertools.get_element_starting_at_exactly_prolated_offset(voice, Duration(6, 8))
        Note("b'8")

    Raise missing component error when no `container` element starts at exactly `prolated_offset`.

    .. versionchanged:: 2.0
        renamed ``containertools.get_element_starting_at_prolated_offset()`` to
        ``containertools.get_element_starting_at_exactly_prolated_offset()``.
    '''

    for element in container:
        if element._offset.start == prolated_offset:
            return element

    raise MissingComponentError
