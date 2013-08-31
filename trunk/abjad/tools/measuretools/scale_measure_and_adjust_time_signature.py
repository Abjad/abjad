# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools


def scale_measure_and_adjust_time_signature(measure, multiplier=1):
    r'''Scales `measure` by `multiplier` and adjusts time signature:

    ..  container:: example

        **Example 1.** Scale measure by non-power-of-two multiplier:

        ::

            >>> measure = Measure((3, 8), "c'8 d'8 e'8")
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

        ::

            >>> measuretools.scale_measure_and_adjust_time_signature(
            ...     measure, Multiplier(2, 3))
            Measure(3/12, [c'8, d'8, e'8])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8
                    d'8
                    e'8
                }
            }

    Returns `measure`.
    '''

    measure.scale_and_adjust_time_signature(multiplier)
    return measure
