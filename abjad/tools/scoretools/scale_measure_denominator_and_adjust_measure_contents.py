# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools


def scale_measure_denominator_and_adjust_measure_contents(measure, factor):
    r'''Scales power-of-two `measure` to non-power-of-two measure 
    with new denominator `factor`:

    ..  container:: example

        **Example.**

        ::

            >>> measure = Measure((2, 8), "c'8 d'8")
            >>> beam = spannertools.BeamSpanner()
            >>> attach(beam, measure.select_leaves())
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 2/8
                c'8 [
                d'8 ]
            }

        ::

            >>> scoretools.scale_measure_denominator_and_adjust_measure_contents(
            ...     measure, 3)
            Measure(3/12, [c'8., d'8.])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8. ]
                }
            }

    Treats new denominator `factor` like clever form of ``1``:
    ``3/3`` or ``5/5`` or ``7/7``, etc.

    Preserves `measure` prolated duration.

    Derives new `measure` multiplier.

    Scales `measure` contents.

    Picks best new time signature.
    '''
    from abjad.tools import scoretools
    from abjad.tools import timesignaturetools
    from abjad.tools.functiontools import attach

    # save old time signature duration
    old_time_signature_duration = measure.time_signature.duration

    # find new time signature
    new_time_signature = \
        measure._duration_and_possible_denominators_to_time_signature(
        old_time_signature_duration, 
        factor=factor,
        )

    # scale contents of measures in expr
    multiplier = new_time_signature.implied_prolation.reciprocal
    measure._scale(multiplier)

    # assign new time signature
    for mark in measure._get_marks(marktools.TimeSignatureMark):
        mark.detach()
    attach(new_time_signature, measure)

    # return measure
    return measure
