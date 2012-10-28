from abjad.tools import mathtools
from abjad.tools import notetools


def fill_measures_in_expr_with_time_signature_denominator_notes(expr, iterctrl=None):
    r'''.. versionadded:: 1.1

    Fill measures in `expr` with time signature denominator notes::

        >>> staff = Staff([Measure((3, 4), []), Measure((3, 16), []), Measure((3, 8), [])])
        >>> measuretools.fill_measures_in_expr_with_time_signature_denominator_notes(staff)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 3/4
                c'4
                c'4
                c'4
            }
            {
                \time 3/16
                c'16
                c'16
                c'16
            }
            {
                \time 3/8
                c'8
                c'8
                c'8
            }
        }

    Delete existing contents of measures in `expr`.

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterationtools.iterate_measures_in_expr(expr)):
        if iterctrl(measure, i):
            time_signature = contexttools.get_effective_time_signature(measure)
            denominator = mathtools.greatest_power_of_two_less_equal(
                time_signature.denominator)
            numerator = time_signature.numerator
            notes = notetools.Note(0, (1, denominator)) * numerator
            measure[:] = notes
