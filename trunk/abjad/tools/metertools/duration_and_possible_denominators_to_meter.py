from abjad.tools import durtools
from abjad.tools import mathtools


def duration_and_possible_denominators_to_meter(duration, denominators = None, factor = None):
    '''Make new meter equal to `duration`::

        abjad> from abjad.tools import metertools

    ::

        abjad> metertools.duration_and_possible_denominators_to_meter(Duration(3, 2))
        TimeSignatureMark(3, 2)

    Make new meter equal to `duration` with denominator equal to the first possible element in `denominators`::

        abjad> metertools.duration_and_possible_denominators_to_meter(Duration(3, 2), denominators = [5, 6, 7, 8])
        TimeSignatureMark(9, 6)

    Make new meter equal to `duration` with denominator divisible by `factor`::

        abjad> metertools.duration_and_possible_denominators_to_meter(Duration(3, 2), factor = 5)
        TimeSignatureMark(15, 10)

    Return new meter.

    .. versionchanged:: 2.0
        renamed ``metertools.make_best()`` to
        ``metertools.duration_and_possible_denominators_to_meter()``.
    '''
    from abjad.tools import contexttools

    if denominators is not None:
        if factor is not None:
            denominators = [d for d in denominators if factor in mathtools.factors(d)]
        for desired_denominator in sorted(denominators):
            candidate_pair = durtools.rational_to_duration_pair_with_specified_integer_denominator(
                duration, desired_denominator)
            if candidate_pair[-1] == desired_denominator:
                return contexttools.TimeSignatureMark(candidate_pair)

    if factor is not None:
        if factor in mathtools.factors(duration.denominator):
            return contexttools.TimeSignatureMark(duration)
        else:
            meter_numerator = factor * duration.numerator
            meter_denominator = factor * duration.denominator
            return contexttools.TimeSignatureMark(meter_numerator, meter_denominator)
    else:
        return contexttools.TimeSignatureMark(duration)


