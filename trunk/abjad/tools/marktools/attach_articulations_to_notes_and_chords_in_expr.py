def attach_articulations_to_notes_and_chords_in_expr(expr, articulations):
    r'''.. versionadded:: 2.0

    Attach `articulations` to notes and chords in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> marktools.attach_articulations_to_notes_and_chords_in_expr(staff, list('^.'))

    ::

        >>> f(staff)
        \new Staff {
            c'8 -\marcato -\staccato
            d'8 -\marcato -\staccato
            e'8 -\marcato -\staccato
            f'8 -\marcato -\staccato
        }

    Return none.
    '''
    # TODO: marktools should be able to import leaftools at top level
    from abjad.tools import iterationtools
    from abjad.tools import marktools

    for leaf in iterationtools.iterate_notes_and_chords_in_expr(expr):
        for articulation in articulations:
            marktools.Articulation(articulation)(leaf)
