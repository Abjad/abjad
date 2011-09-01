from abjad.tools.marktools.Articulation import Articulation


def attach_articulations_to_notes_and_chords_in_expr(expr, articulations):
    r'''.. versionadded:: 2.0

    Attach `articulations` to notes and chords in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.attach_articulations_to_notes_and_chords_in_expr(staff, list('^.'))

    ::

        abjad> f(staff)
        \new Staff {
            c'8 -\marcato -\staccato
            d'8 -\marcato -\staccato
            e'8 -\marcato -\staccato
            f'8 -\marcato -\staccato
        }

    Return none.
    '''
    from abjad.tools import leaftools

    for leaf in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
        for articulation in articulations:
            Articulation(articulation)(leaf)
