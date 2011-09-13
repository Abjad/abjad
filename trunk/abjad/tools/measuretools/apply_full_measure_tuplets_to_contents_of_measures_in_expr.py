from abjad.tools.measuretools._apply_full_measure_tuplets_to_contents_of_measures_in_expr import _apply_full_measure_tuplets_to_contents_of_measures_in_expr


def apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr):
    r'''.. versionadded:: 2.0

    Apply full-measure tuplets to contents of measures in `expr`::

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

        abjad> measuretools.apply_full_measure_tuplets_to_contents_of_measures_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                {
                    c'8
                    d'8
                }
            }
            {
                \time 3/8
                {
                    e'8
                    f'8
                    g'8
                }
            }
        }

    Return none.
    '''

    return _apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr, supplement = None)
