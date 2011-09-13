from abjad.tools import mathtools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def fill_measures_in_expr_with_meter_denominator_notes(expr, iterctrl = None):
    r'''.. versionadded:: 1.1

    Fill measures in `expr` with meter denominator notes::

        abjad> staff = Staff([Measure((3, 4), []), Measure((3, 16), []), Measure((3, 8), [])])
        abjad> measuretools.fill_measures_in_expr_with_meter_denominator_notes(staff)

    ::

        abjad> f(staff)
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
    from abjad.tools.notetools.Note import Note
    from abjad.tools import contexttools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterate_measures_forward_in_expr(expr)):
        if iterctrl(measure, i):
            meter = contexttools.get_effective_time_signature(measure)
            denominator = mathtools.greatest_power_of_two_less_equal(
                meter.denominator)
            numerator = meter.numerator
            notes = Note(0, (1, denominator)) * numerator
            measure[:] = notes
