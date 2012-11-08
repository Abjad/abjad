from abjad.tools import notetools


def fill_measures_in_expr_with_minimal_number_of_notes(expr, decrease_durations_monotonically=True, iterctrl=None):
    '''.. versionadded:: 1.1

    Fill measures in `expr` with minimal number of notes that decrease durations monotonically::

        >>> measure = Measure((5, 18), [])

    ::

        >>> measuretools.fill_measures_in_expr_with_minimal_number_of_notes(
        ...     measure, decrease_durations_monotonically=True)

    ::

        >>> f(measure)
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'4 ~
                c'16
            }
        }

    Fill measures in `expr` with minimal number of notes that increase durations monotonically::

        >>> measure = Measure((5, 18), [])

    ::

        >>> measuretools.fill_measures_in_expr_with_minimal_number_of_notes(
        ...     measure, decrease_durations_monotonically=False)

    ::

        >>> f(measure)
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'16 ~
                c'4
            }
        }

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterationtools.iterate_measures_in_expr(expr)):
        if iterctrl(measure, i):
            time_signature = contexttools.get_effective_time_signature(measure)
            written_duration = time_signature.duration / time_signature.implied_prolation
            notes = notetools.make_notes(0, written_duration, decrease_durations_monotonically=decrease_durations_monotonically)
            measure[:] = notes
