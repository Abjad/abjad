from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def duration_and_possible_denominators_to_time_signature(preprolated_duration, denominators=None, factor=None):
    '''Make new time signature equal to `preprolated_duration`::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(
        ...     Duration(3, 2))
        TimeSignatureMark((3, 2))

    Make new time signature equal to `preprolated_duration` with denominator equal to the
    first possible element in `denominators`::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(
        ...     Duration(3, 2), denominators=[5, 6, 7, 8])
        TimeSignatureMark((9, 6))

    Make new time signature equal to `preprolated_duration` with denominator divisible by
    `factor`::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(
        ...     Duration(3, 2), factor=5)
        TimeSignatureMark((15, 10))

    .. note:: possibly divide this into two separate functions?

    Return new time signature.
    '''

    # check input
    preprolated_duration = durationtools.Duration(preprolated_duration)

    if denominators is not None:
        if factor is not None:
            denominators = [d for d in denominators if factor in mathtools.factors(d)]
        for desired_denominator in sorted(denominators):
            nonreduced_fraction = mathtools.NonreducedFraction(preprolated_duration)
            candidate_pair = nonreduced_fraction.with_denominator(desired_denominator)
            if candidate_pair.denominator == desired_denominator:
                return contexttools.TimeSignatureMark(candidate_pair)
    if factor is not None:
        if factor in mathtools.factors(preprolated_duration.denominator):
            return contexttools.TimeSignatureMark(preprolated_duration)
        else:
            time_signature_numerator = factor * preprolated_duration.numerator
            time_signature_denominator = factor * preprolated_duration.denominator
            return contexttools.TimeSignatureMark((time_signature_numerator, time_signature_denominator))
    else:
        return contexttools.TimeSignatureMark(preprolated_duration)
