from abjad.tools import contexttools
from abjad.tools import durationtools


def scale_measure_denominator_and_adjust_measure_contents(measure, factor):
    r'''.. versionadded:: 1.1

    Change power-of-two `measure` to non-power-of-two measure with new denominator `factor`::

        >>> measure = Measure((2, 8), "c'8 d'8")
        >>> beamtools.BeamSpanner(measure.leaves)
        BeamSpanner(c'8, d'8)

    ::

        >>> f(measure)
        {
            \time 2/8
            c'8 [
            d'8 ]
        }

    ::

        >>> measuretools.scale_measure_denominator_and_adjust_measure_contents(measure, 3)
        Measure(3/12, [c'8., d'8.])

    ::

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
    old_time_signature_duration = contexttools.get_effective_time_signature(measure).duration

    # find new time signature
    new_time_signature = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        old_time_signature_duration, factor=factor)

    # scale contents of measures in expr
    measuretools.scale_contents_of_measures_in_expr(measure, new_time_signature.implied_prolation.reciprocal)

    # assign new time signature
    contexttools.detach_time_signature_marks_attached_to_component(measure)
    new_time_signature.attach(measure)

    # return measure
    return measure
