from abjad.tools import mathtools


def get_nonbinary_factor_from_meter_denominator(meter):
    '''Get nonbinary factor from nonbinary `meter` denominator::

        abjad> from abjad.tools import metertools

    ::

        abjad> metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 12))
        3

    ::

        abjad> metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 13))
        13

    ::

        abjad> metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 14))
        7

    ::

        abjad> metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 15))
        15

    Get ``1`` from binary `meter` denominator::

        abjad> metertools.get_nonbinary_factor_from_meter_denominator(contexttools.TimeSignatureMark(3, 16))
        1

    Return nonnegative integer.
    '''
    from abjad.tools import contexttools

    ## check input
    assert isinstance(meter, contexttools.TimeSignatureMark)

    ## get nonbinary factor from meter denominator
    nonbinary_factor = mathtools.remove_powers_of_two(meter.denominator)

    ## return nonbinary factor
    return nonbinary_factor


