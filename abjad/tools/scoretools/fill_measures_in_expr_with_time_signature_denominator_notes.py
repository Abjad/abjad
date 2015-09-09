# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.topleveltools import iterate


def fill_measures_in_expr_with_time_signature_denominator_notes(
    expr, iterctrl=None):
    r'''Fill measures in `expr` with time signature denominator notes:

    ::

        >>> staff = Staff([Measure((3, 4), []), Measure((3, 16), []), Measure((3, 8), [])])
        >>> scoretools.fill_measures_in_expr_with_time_signature_denominator_notes(staff)

    ..  doctest::

        >>> print(format(staff))
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

    Returns none.
    '''
    from abjad.tools import scoretools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterate(expr).by_class(scoretools.Measure)):
        if iterctrl(measure, i):
            time_signature = measure.time_signature
            denominator = mathtools.greatest_power_of_two_less_equal(
                time_signature.denominator)
            numerator = time_signature.numerator
            notes = scoretools.Note(0, (1, denominator)) * numerator
            measure[:] = notes
