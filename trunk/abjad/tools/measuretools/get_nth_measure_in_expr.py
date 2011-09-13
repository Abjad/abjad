from abjad.tools.measuretools.Measure import Measure
from abjad.tools.componenttools.get_nth_component_in_expr import get_nth_component_in_expr


# TODO: implement measuretools.iterate_measures_forward_in_expr(expr, i = 0, j = None).
def get_nth_measure_in_expr(expr, n = 0):
    r'''.. versionadded:: 2.0

    Get nth measure in `expr`::

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

    Read forward for positive values of `n`. ::

        abjad> for n in range(3):
        ...     measuretools.get_nth_measure_in_expr(staff, n)
        ...
        Measure(2/8, [c'8, d'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [g'8, a'8])

    Read backward for negative values of `n`. ::

        abjad> for n in range(3, -1, -1):
        ...     measuretools.get_nth_measure_in_expr(staff, n)
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    .. versionchanged:: 2.0
        renamed ``iterate.get_nth_measure()`` to
        ``measuretools.get_nth_measure_in_expr()``.
    '''

    return get_nth_component_in_expr(expr, Measure, n)
