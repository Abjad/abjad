def remove_outer_rests_from_sequence(sequence):
    r'''.. versionadded:: 2.0

    Remove outer rests from `sequence`::

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

        >>> leaftools.remove_outer_rests_from_sequence(staff)
        [Note("c'8"), Note("d'8")]

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
    from abjad.tools import leaftools
    from abjad.tools import resttools

    result = leaftools.remove_terminal_rests_from_sequence(sequence)
    initial_rests_to_remove = 0

    for element in result:
        if isinstance(element, resttools.Rest):
            initial_rests_to_remove += 1
        else:
            break

    result = result[initial_rests_to_remove:]
    return result
