def apply_full_measure_tuplets_to_contents_of_measures_in_expr(expr):
    r'''.. versionadded:: 2.0

    Apply full-measure tuplets to contents of measures in `expr`::

        >>> staff = Staff([Measure((2, 8), "c'8 d'8"), Measure((3, 8), "e'8 f'8 g'8")])

    ::

        >>> f(staff)
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

        >>> measuretools.apply_full_measure_tuplets_to_contents_of_measures_in_expr(staff)

    ::

        >>> f(staff)
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
    from abjad.tools import iterationtools
    from abjad.tools import tuplettools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        target_duration = measure.preprolated_duration
        tuplet = tuplettools.FixedDurationTuplet(target_duration, measure[:])
