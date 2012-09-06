from abjad.tools import contexttools
from abjad.tools import mathtools


def get_nonbinary_factor_from_time_signature_denominator(time_signature):
    '''Get nonbinary factor from nonbinary `time_signature` denominator::

        >>> from abjad.tools import timesignaturetools

    ::

        >>> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 12)))
        3

    ::

        >>> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 13)))
        13

    ::

        >>> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 14)))
        7

    ::

        >>> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 15)))
        15

    Get ``1`` from binary `time_signature` denominator::

        >>> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(
        ... contexttools.TimeSignatureMark((3, 16)))
        1

    Return nonnegative integer.
    '''
    # check input
    assert isinstance(time_signature, contexttools.TimeSignatureMark)

    # get nonbinary factor from time signature denominator
    nonbinary_factor = mathtools.remove_powers_of_two(time_signature.denominator)

    # return nonbinary factor
    return nonbinary_factor
