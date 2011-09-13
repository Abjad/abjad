from abjad.tools.leaftools.remove_terminal_rests_from_sequence import remove_terminal_rests_from_sequence


def remove_outer_rests_from_sequence(sequence):
    r'''.. versionadded:: 2.0

    Remove outer rests from `sequence`::

        abjad> staff = Staff("r8 r8 c'8 d'8 r4 r4")

    ::

        abjad> f(staff)
        \new Staff {
            r8
            r8
            c'8
            d'8
            r4
            r4
        }

    ::

        abjad> leaftools.remove_outer_rests_from_sequence(staff)
        [Note("c'8"), Note("d'8")]

    ::

        abjad> f(staff)
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
    from abjad.tools.resttools.Rest import Rest

    result = remove_terminal_rests_from_sequence(sequence)
    initial_rests_to_remove = 0

    for element in result:
        if isinstance(element, Rest):
            initial_rests_to_remove += 1
        else:
            break

    result = result[initial_rests_to_remove:]
    return result
