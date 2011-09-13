from abjad.tools.notetools.Note import Note
from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr


def iterate_notes_backward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Yield right-to-left notes in `expr`::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
        }

    ::

        abjad> for leaf in notetools.iterate_notes_backward_in_expr(staff):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    Use optional `start` and `stop` keyword parameters to control
    indices of iteration::

        abjad> for leaf in notetools.iterate_notes_backward_in_expr(staff, start = 3):
        ...     leaf
        ...
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        abjad> for leaf in notetools.iterate_notes_backward_in_expr(staff, start = 0, stop = 3):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")

    ::

        abjad> for leaf in notetools.iterate_notes_backward_in_expr(staff, start = 2, stop = 4):
        ...     leaf
        ...
        Note("f'8")
        Note("e'8")

    Return note generator.

    .. versionchanged:: 2.0
        renamed ``iterate.notes_backward_in()`` to
        ``notetools.iterate_notes_backward_in_expr()``.
    '''

    return iterate_components_backward_in_expr(expr, Note, start = start, stop = stop)
