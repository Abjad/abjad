from abjad.tools import contexttools


def make_repeated_skips_from_time_signature(time_signature):
    '''.. versionadded:: 2.0

    Make repeated skips from `time_signature`::

        >>> skiptools.make_repeated_skips_from_time_signature((5, 32))
        [Skip('s32'), Skip('s32'), Skip('s32'), Skip('s32'), Skip('s32')]

    Return list of skips.
    '''
    from abjad.tools import skiptools

    # afford basic input polymorphism
    time_signature = contexttools.TimeSignatureMark(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        raise NotImplementedError(
            'TODO: extend this function for time signatures with non-power-of-two denominators.')

    # make and return repeated skips
    return time_signature.numerator * skiptools.Skip((1, time_signature.denominator))
