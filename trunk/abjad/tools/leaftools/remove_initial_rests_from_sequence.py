def remove_initial_rests_from_sequence(sequence):
    r'''.. versionadded:: 2.0

    Remove initial rests from `sequence`::

        >>> staff = Staff("r8 r8 c'8 d'8 r4 r4")

    ::

        >>> f(staff)
        \new Staff {
            r8
            r8
            c'8
            d'8
            r4
            r4
        }

    ::

        >>> leaftools.remove_initial_rests_from_sequence(staff)
        [Note("c'8"), Note("d'8"), Rest('r4'), Rest('r4')]

    ::

        >>> f(staff)
        \new Staff {
            r8
            r8
            c'8
            d'8
            r4
            r4
        }

    Return list.
    '''
    from abjad.tools import resttools

    result = []
    found_nonrest = False

    for element in sequence:
        if not isinstance(element, resttools.Rest):
            found_nonrest = True
        if found_nonrest:
            result.append(element)

    return result
