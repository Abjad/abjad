# -*- encoding: utf-8 -*-
from abjad.tools import selectiontools


def make_spacer_skip_measures(time_signatures):
    r'''Make measures with full-measure spacer skips from `time_signatures`.

    ..  container:: example

        ::

            >>> measures = scoretools.make_spacer_skip_measures(
            ...     [(1, 8), (5, 16), (5, 16)])
            >>> staff = Staff(measures)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
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

    Returns selection of unincorporated measures.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools

    # check input
    time_signatures = [
        indicatortools.TimeSignature(x) for x in time_signatures]

    # make measures
    measures = [scoretools.Measure(x, []) for x in time_signatures]
    scoretools.fill_measures_in_expr_with_full_measure_spacer_skips(measures)

    # return measures
    measures = selectiontools.Selection(measures)
    return measures
