from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def duration_and_possible_denominators_to_time_signature(duration, denominators=None, factor=None):
    '''Make new time_signature equal to `duration`::

        >>> from abjad.tools import timesignaturetools

    ::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(Duration(3, 2))
        TimeSignatureMark((3, 2))

    Make new time_signature equal to `duration` with denominator equal to the first possible 
    element in `denominators`::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(
        ... Duration(3, 2), denominators=[5, 6, 7, 8])
        TimeSignatureMark((9, 6))

    Make new time_signature equal to `duration` with denominator divisible by `factor`::

        >>> timesignaturetools.duration_and_possible_denominators_to_time_signature(
        ... Duration(3, 2), factor=5)
        TimeSignatureMark((15, 10))

    Return new time_signature.

    .. versionchanged:: 2.0
        renamed ``timesignaturetools.make_best()`` to
        ``timesignaturetools.duration_and_possible_denominators_to_time_signature()``.
    '''
    if denominators is not None:
        if factor is not None:
            denominators = [d for d in denominators if factor in mathtools.factors(d)]
        for desired_denominator in sorted(denominators):
            nonreduced_fraction = mathtools.NonreducedFraction(duration)
            candidate_pair = nonreduced_fraction.with_denominator(desired_denominator)
            if candidate_pair.denominator == desired_denominator:
                return contexttools.TimeSignatureMark(candidate_pair)

    if factor is not None:
        if factor in mathtools.factors(duration.denominator):
            return contexttools.TimeSignatureMark(duration)
        else:
            time_signature_numerator = factor * duration.numerator
            time_signature_denominator = factor * duration.denominator
            return contexttools.TimeSignatureMark((time_signature_numerator, time_signature_denominator))
    else:
        return contexttools.TimeSignatureMark(duration)
