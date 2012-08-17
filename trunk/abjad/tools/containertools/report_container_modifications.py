def report_container_modifications(container):
    r'''Report `container` modifications as string:

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")
        >>> container.override.note_head.color = 'red'
        >>> container.override.note_head.style = 'harmonic'

    ::

        >>> f(container)
        {
            \override NoteHead #'color = #red
            \override NoteHead #'style = #'harmonic
            c'8
            d'8
            e'8
            f'8
            \revert NoteHead #'color
            \revert NoteHead #'style
        }

    ::

        >>> string = containertools.report_container_modifications(container)

    ::

        >>> print string
        {
            \override NoteHead #'color = #red
            \override NoteHead #'style = #'harmonic
            %%% 4 components omitted %%%
            \revert NoteHead #'color
            \revert NoteHead #'style
        }

    Return string.
    '''
    from abjad.tools import containertools
    from abjad.tools import formattools

    assert isinstance(container, containertools.Container)

    fc = formattools.get_all_format_contributions(container)

    result = []

    result.extend(container._get_format_contributions_for_slot('before', fc))
    result.extend(container._get_format_contributions_for_slot('open brackets', fc))
    result.extend(container._get_format_contributions_for_slot('opening', fc))
    result.append('\t%%%%%% %s components omitted %%%%%%' % len(container))
    result.extend(container._get_format_contributions_for_slot('closing', fc))
    result.extend(container._get_format_contributions_for_slot('close brackets', fc))
    result.extend(container._get_format_contributions_for_slot('after', fc))

    result = '\n'.join(result)

    return result
