from abjad.tools.containertools._report_container_modifications import _report_container_modifications


def report_container_modifications_as_string(container):
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

        >>> string = containertools.report_container_modifications_as_string(container)

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

    return _report_container_modifications(container, output='string')
