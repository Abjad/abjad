from abjad.tools import contexttools
from abjad.tools.measuretools.Measure import Measure
from abjad.tools.measuretools.fill_measures_in_expr_with_full_measure_spacer_skips import fill_measures_in_expr_with_full_measure_spacer_skips


def make_measures_with_full_measure_spacer_skips(time_signatures):
    r'''.. versionadded:: 1.1

    Make measures with full-measure spacer skips from `time_signatures`::

        abjad> measures = measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16)])

    ::

        abjad> staff = Staff(measures)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 1/8
                s1 * 1/8
            }
            {
                \time 5/16
                s1 * 5/16
            }
            {
                s1 * 5/16
            }
        }

    Return list of rigid measures.

    .. versionchanged:: 2.0
        renamed ``measuretools.make()`` to
        ``measuretools.make_measures_with_full_measure_spacer_skips()``.
    '''

    # check input
    time_signatures = [contexttools.TimeSignatureMark(x) for x in time_signatures]

    # make measures
    measures = [Measure(x, []) for x in time_signatures]
    fill_measures_in_expr_with_full_measure_spacer_skips(measures)

    # return measures
    return measures
