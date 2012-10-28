import fractions
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def time_signature_to_time_signature_with_power_of_two_denominator(
    time_signature, contents_multiplier=fractions.Fraction(1)):
    '''Change `time_signature` to time signature with power_of_two denominator::

        >>> timesignaturetools.time_signature_to_time_signature_with_power_of_two_denominator(
        ...         contexttools.TimeSignatureMark((3, 12)))
        TimeSignatureMark((2, 8))

    Preserve power_of_two `time_signature`::

        >>> timesignaturetools.time_signature_to_time_signature_with_power_of_two_denominator(
        ...     contexttools.TimeSignatureMark((2, 8)))
        TimeSignatureMark((2, 8))

    Return newly constructed time_signature.
    '''

    # check input
    assert isinstance(time_signature, contexttools.TimeSignatureMark)
    assert isinstance(contents_multiplier, fractions.Fraction)

    # save non_power_of_two time_signature and denominator
    non_power_of_two_denominator = time_signature.denominator

    # find power_of_two denominator
    if contents_multiplier == fractions.Fraction(1):
        power_of_two_denominator = mathtools.greatest_power_of_two_less_equal(non_power_of_two_denominator)
    else:
        power_of_two_denominator = mathtools.greatest_power_of_two_less_equal(non_power_of_two_denominator, 1)

    # find power_of_two pair
    non_power_of_two_pair = mathtools.NonreducedFraction(time_signature.numerator, time_signature.denominator)
    power_of_two_pair = non_power_of_two_pair.with_denominator(power_of_two_denominator)

    # return new power_of_two time_signature
    return contexttools.TimeSignatureMark(power_of_two_pair)
