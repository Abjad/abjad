from abjad.tools import contexttools
from abjad.tools import mathtools


def get_non_power_of_two_factor_from_time_signature_denominator(time_signature):
    '''Get non-power-of-two factor from `time_signature` denominator::

        >>> timesignaturetools.get_non_power_of_two_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 12)))
        3

    ::

        >>> timesignaturetools.get_non_power_of_two_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 13)))
        13

    ::

        >>> timesignaturetools.get_non_power_of_two_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 14)))
        7

    ::

        >>> timesignaturetools.get_non_power_of_two_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 15)))
        15

    Get ``1`` from power_of_two `time_signature` denominator::

        >>> timesignaturetools.get_non_power_of_two_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 16)))
        1

    Return nonnegative integer.
    '''
    # check input
    assert isinstance(time_signature, contexttools.TimeSignatureMark)

    # get non_power_of_two factor from time signature denominator
    non_power_of_two_factor = mathtools.remove_powers_of_two(time_signature.denominator)

    # return non_power_of_two factor
    return non_power_of_two_factor
