from abjad.tools.measuretools._apply_full_measure_tuplets_to_contents_of_measures_in_expr import _apply_full_measure_tuplets_to_contents_of_measures_in_expr


def extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents(expr, supplement):
    r'''.. versionadded:: 2.0

    Extend measures in `expr` with `supplement` and apply full-measure tuplets to contents
    of measures::

        abjad> staff = Staff([Measure((2, 8), "c'8 d'8"), Measure((3, 8), "e'8 f'8 g'8")])

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/8
                e'8
                f'8
                g'8
            }
        }

    ::

        abjad> supplement = [Rest((1, 16))]
        abjad> measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents(staff, supplement)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                \times 4/5 {
                    c'8
                    d'8
                    r16
                }
            }
            {
                \time 3/8
                \fraction \times 6/7 {
                    e'8
                    f'8
                    g'8
                    r16
                }
            }
        }

    Return none.
    '''

    return _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement)
