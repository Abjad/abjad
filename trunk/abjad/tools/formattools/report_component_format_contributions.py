def report_component_format_contributions(component, verbose=False):
    r'''.. versionadded:: 1.1

    Report `component` format contributions:

        >>> staff = Staff("c'4 [ ( d'4 e'4 f'4 ] )")
        >>> staff[0].override.note_head.color = 'red'

    ::

        >>> print formattools.report_component_format_contributions(staff[0])
        slot 1:
            grob overrides:
                \once \override NoteHead #'color = #red
        slot 3:
        slot 4:
            leaf body:
                c'4 [ (
        slot 5:
        slot 7:
        <BLANKLINE>

    Return string.
    '''
    return component._report_format_contributors()
