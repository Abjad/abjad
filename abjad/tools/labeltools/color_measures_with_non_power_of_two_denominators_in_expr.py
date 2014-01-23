# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def color_measures_with_non_power_of_two_denominators_in_expr(
    expr, 
    color='red',
    ):
    r'''Colors measures with non-power-of-two denominators in `expr` 
    with `color`.

    ::

        >>> staff = Staff(2 * Measure((2, 8), "c'8 d'8"))
        >>> scoretools.scale_measure_denominator_and_adjust_measure_contents(staff[1], 3)
        Measure((3, 12), "c'8. d'8.", implicit_scaling=True)

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8.
                    d'8.
                }
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> labeltools.color_measures_with_non_power_of_two_denominators_in_expr(staff, 'red')
        [Measure((3, 12), "c'8. d'8.", implicit_scaling=True)]

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \override Beam #'color = #red
                \override Dots #'color = #red
                \override NoteHead #'color = #red
                \override Staff.TimeSignature #'color = #red
                \override Stem #'color = #red
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8.
                    d'8.
                }
                \revert Beam #'color
                \revert Dots #'color
                \revert NoteHead #'color
                \revert Staff.TimeSignature #'color
                \revert Stem #'color
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns list of measures colored.

    Color names appear in LilyPond Learning Manual appendix B.5.
    '''
    from abjad.tools import labeltools

    # init measures colored
    measures_colored = []

    # color non-power-of-two measures in expr
    for measure in iterate(expr).by_class(scoretools.Measure):
        if measure.time_signature.has_non_power_of_two_denominator:
            labeltools.color_measure(measure, color)
            measures_colored.append(measure)

    # return measures colored
    return measures_colored
