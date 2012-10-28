from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def is_equivalent_to_time_signature_with_power_of_two_denominator(expr):
    '''True when `expr` is a meter with binary-valued duration::

        >>> from abjad.tools import timesignaturetools

    ::

        >>> timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(
        ... contexttools.TimeSignatureMark((3, 12)))
        True

    Otherwise false::

        >>> timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(
        ... contexttools.TimeSignatureMark((4, 12)))
        False

    ::

        >>> timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator('text')
        False

    Return boolean.
    '''
    # check input
    if not isinstance(expr, contexttools.TimeSignatureMark):
        return False

    # express meter as rational and reduce to relatively prime terms
    meter_as_rational = durationtools.Duration(expr.numerator, expr.denominator)

    # return True if reduced meter denominator is power of two
    return mathtools.is_nonnegative_integer_power_of_two(meter_as_rational.denominator)
