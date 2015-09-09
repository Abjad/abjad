# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def fill_measures_in_expr_with_minimal_number_of_notes(
    expr,
    decrease_durations_monotonically=True,
    iterctrl=None,
    ):
    '''Fills measures in `expr` with minimal number of notes that decrease
    durations monotonically:

    ::

        >>> measure = Measure((5, 18), [], implicit_scaling=True)

    ::

        >>> scoretools.fill_measures_in_expr_with_minimal_number_of_notes(
        ...     measure, decrease_durations_monotonically=True)

    ..  doctest::

        >>> print(format(measure))
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'4 ~
                c'16
            }
        }

    Fill measures in `expr` with minimal number of notes that increase
    durations monotonically:

    ::

        >>> measure = Measure((5, 18), [])
        >>> measure.implicit_scaling = True

    ::

        >>> scoretools.fill_measures_in_expr_with_minimal_number_of_notes(
        ...     measure, decrease_durations_monotonically=False)

    ..  doctest::

        >>> print(format(measure))
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'16 ~
                c'4
            }
        }

    Returns none.
    '''
    from abjad.tools import scoretools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterate(expr).by_class(scoretools.Measure)):
        if iterctrl(measure, i):
            time_signature = measure.time_signature
            written_duration = time_signature.duration / time_signature.implied_prolation
            notes = scoretools.make_notes(
                0,
                written_duration,
                decrease_durations_monotonically=decrease_durations_monotonically)
            measure[:] = notes
