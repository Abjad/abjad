def remove_terminal_rests_from_sequence(sequence):
    r'''.. versionadded:: 2.0

    Remove terminal rests from `sequence`::

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

        abjad> leaftools.remove_terminal_rests_from_sequence(staff)
        [Rest('r8'), Rest('r8'), Note("c'8"), Note("d'8")]

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

    result = []
    found_nonrest = False

    for element in reversed(sequence):
        if not isinstance(element, Rest):
            found_nonrest = True
        if found_nonrest:
            result.insert(0, element)

    return result
