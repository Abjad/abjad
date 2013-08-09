# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.selectiontools import more


def scale_measure_denominator_and_adjust_measure_contents(measure, factor):
    r'''Change power-of-two `measure` to non-power-of-two measure with new denominator `factor`:

    ::

        >>> measure = Measure((2, 8), "c'8 d'8")
        >>> spannertools.BeamSpanner(measure.select_leaves())
        BeamSpanner(c'8, d'8)

    ..  doctest::

        >>> f(measure)
        {
            \time 2/8
            c'8 [
            d'8 ]
        }

    ::

        >>> measuretools.scale_measure_denominator_and_adjust_measure_contents(measure, 3)
        Measure(3/12, [c'8., d'8.])

    ..  doctest::

        >>> f(measure)
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8. [
                d'8. ]
            }
        }


    Treat new denominator `factor` like clever form of ``1``:
    ``3/3`` or ``5/5`` or ``7/7``, etc.

    Preserve `measure` prolated duration.

    Derive new `measure` multiplier.

    Scale `measure` contents.

    Pick best new time signature.
    '''
    from abjad.tools import measuretools
    from abjad.tools import timesignaturetools

    # save old time signature duration
    old_time_signature_duration = measure.time_signature.duration

    # find new time signature
    new_time_signature = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        old_time_signature_duration, factor=factor)

    # scale contents of measures in expr
    measuretools.scale_contents_of_measures_in_expr(measure, new_time_signature.implied_prolation.reciprocal)

    # assign new time signature
    measure.select().detach_marks(contexttools.TimeSignatureMark)
    new_time_signature.attach(measure)

    # return measure
    return measure
