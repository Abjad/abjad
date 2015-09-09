# -*- coding: utf-8 -*-
from abjad.tools import selectiontools


def make_spacer_skip_measures(time_signatures, implicit_scaling=False):
    r'''Makes measures with full-measure spacer skips from `time_signatures`.

    ..  container:: example

        ::

            >>> measures = scoretools.make_spacer_skip_measures(
            ...     [(1, 8), (5, 16), (5, 16)])
            >>> staff = Staff(measures)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

    # make measures
    measures = []
    for time_signature in time_signatures:
        time_signature = indicatortools.TimeSignature(time_signature)
        measure = scoretools.Measure(
            time_signature,
            implicit_scaling=implicit_scaling,
            )
        measures.append(measure)
    scoretools.fill_measures_in_expr_with_full_measure_spacer_skips(measures)

    # return measures
    measures = selectiontools.Selection(measures)
    return measures
