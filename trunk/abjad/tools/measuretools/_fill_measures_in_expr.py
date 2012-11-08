import numbers
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools


# TODO: remove function entirely
def _fill_measures_in_expr(expr, mode, iterctrl=lambda measure, i: True):
    '''Populate each measure in 'expr' according to 'mode'.

    With mode = 'decrease_durations_monotonically':
        Populate with decrease_durations_monotonically series of notes
        summing to duration of effective time signature of measure.

    With mode = 'increase_durations_monotonically':
        Populate with increase_durations_monotonically series of notes
        summing to duration of effective time signature of measure.

    With mode = 'time signature series':
        Populate with n total 1/d notes, where
        n equals effective_time_signature.numerator, and
        d equals effective_time_signature.denominator.

    With mode = 'skip':
        Populate with exactly one skip, such that
        skip.prolated_duration == effective_time_signature.duration.
        Remove spanners attaching to measure.

    When mode is None:
        Empty the contents of each measure.

    .. versionchanged:: 2.0
        renamed ``measuretools.populate()``
        to ``measuretools._fill_measures_in_expr()``.
    '''

    if mode == 'decrease_durations_monotonically':
        _measures_populate_decrease_durations_monotonically(expr, iterctrl)
    elif mode == 'increase_durations_monotonically':
        _measures_populate_increase_durations_monotonically(expr, iterctrl)
    elif mode == 'time signature series':
        _measures_populate_time_signature(expr, iterctrl)
    elif mode == 'skip':
        _measures_populate_skip(expr, iterctrl)
    elif isinstance(mode, (numbers.Number, tuplet)):
        _measures_populate_duration_train(expr, mode, iterctrl)
    elif mode is None:
        _measures_populate_none(expr, iterctrl)
    else:
        raise ValueError('unknown measure population mode "%s".' % mode)
