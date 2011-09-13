from abjad.tools import contexttools
from abjad.tools.measuretools.color_measure import color_measure
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def color_nonbinary_measures_in_expr(expr, color = 'red'):
    r'''.. versionadded:: 2.0

    Color nonbinary measures in `expr` with `color`::

        abjad> staff = Staff(Measure((2, 8), "c'8 d'8") * 2)
        abjad> measuretools.scale_measure_denominator_and_adjust_measure_contents(staff[1], 3)
        Measure(3/12, [c'8., d'8.])

    ::

        abjad> f(staff)
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

        abjad> measuretools.color_nonbinary_measures_in_expr(staff, 'red')
        [Measure(3/12, [c'8., d'8.])]

    ::

        abjad> f(staff)
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

    Return list of measures colored.

    Color names appear in LilyPond Learning Manual appendix B.5.
    '''

    # init measures colored
    measures_colored = []

    # color nonbinary measures in expr
    for measure in iterate_measures_forward_in_expr(expr):
        if contexttools.get_effective_time_signature(measure).is_nonbinary:
            color_measure(measure, color)
            measures_colored.append(measure)

    # return measures colored
    return measures_colored
