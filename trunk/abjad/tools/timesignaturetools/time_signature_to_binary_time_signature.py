from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
import fractions


def time_signature_to_binary_time_signature(nonbinary_meter, contents_multiplier = fractions.Fraction(1)):
    '''Change nonbinary `meter` to binary meter::

        abjad> from abjad.tools import timesignaturetools

    ::

        abjad> timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((3, 12)))
        TimeSignatureMark((2, 8))

    Preserve binary `meter`::

        abjad> timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((2, 8)))
        TimeSignatureMark((2, 8))

    Return newly constructed meter.

    .. versionchanged:: 2.0
        renamed ``timesignaturetools.make_binary()`` to
        ``timesignaturetools.time_signature_to_binary_time_signature()``.
    '''

    # check input
    assert isinstance(nonbinary_meter, contexttools.TimeSignatureMark)
    assert isinstance(contents_multiplier, fractions.Fraction)

    # save nonbinary meter and denominator
    nonbinary_denominator = nonbinary_meter.denominator

    # find binary denominator
    if contents_multiplier == fractions.Fraction(1):
        binary_denominator = mathtools.greatest_power_of_two_less_equal(nonbinary_denominator)
    else:
        binary_denominator = mathtools.greatest_power_of_two_less_equal(nonbinary_denominator, 1)

    # find binary pair
    nonbinary_pair = (nonbinary_meter.numerator, nonbinary_meter.denominator)
    binary_pair = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
        nonbinary_pair, binary_denominator)

    # return new binary meter
    return contexttools.TimeSignatureMark(binary_pair)
