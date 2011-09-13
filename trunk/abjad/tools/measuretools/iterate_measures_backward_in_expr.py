from abjad.tools.measuretools.Measure import Measure
from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr


def iterate_measures_backward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate measures backward in `expr`::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

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

        abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    Use the optional `start` and `stop` keyword parameters
    to control indices of iteration. ::

        abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff, start = 1):
        ...     measure
        ...
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    ::

        abjad> for measure in measuretools.iterate_measures_backward_in_expr(staff, start = 0, stop = 2):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])

    .. versionchanged:: 2.0
        renamed ``iterate.measures_backward_in()`` to
        ``measuretools.iterate_measures_backward_in_expr()``.
    '''

    return iterate_components_backward_in_expr(expr, Measure, start = start, stop = stop)
