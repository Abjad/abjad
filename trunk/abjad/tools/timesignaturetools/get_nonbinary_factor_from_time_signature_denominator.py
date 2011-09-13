from abjad.tools import mathtools


def get_nonbinary_factor_from_time_signature_denominator(meter):
    '''Get nonbinary factor from nonbinary `meter` denominator::

        abjad> from abjad.tools import timesignaturetools

    ::

        abjad> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 12)))
        3

    ::

        abjad> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 13)))
        13

    ::

        abjad> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 14)))
        7

    ::

        abjad> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 15)))
        15

    Get ``1`` from binary `meter` denominator::

        abjad> timesignaturetools.get_nonbinary_factor_from_time_signature_denominator(contexttools.TimeSignatureMark((3, 16)))
        1

    Return nonnegative integer.
    '''
    from abjad.tools import contexttools

    # check input
    assert isinstance(meter, contexttools.TimeSignatureMark)

    # get nonbinary factor from meter denominator
    nonbinary_factor = mathtools.remove_powers_of_two(meter.denominator)

    # return nonbinary factor
    return nonbinary_factor
