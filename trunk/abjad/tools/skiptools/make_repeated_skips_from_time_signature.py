from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark
from abjad.tools.skiptools.Skip import Skip


def make_repeated_skips_from_time_signature(time_signature):
    '''.. versionadded:: 2.0

    Make repeated skips from `time_signature`::

        abjad> skiptools.make_repeated_skips_from_time_signature((5, 32))
        [Skip('s32'), Skip('s32'), Skip('s32'), Skip('s32'), Skip('s32')]

    Return list of skips.
    '''

    # afford basic input polymorphism
    time_signature = TimeSignatureMark(time_signature)

    # check input
    if time_signature.is_nonbinary:
        raise NotImplementedError('TODO: extend this function for nonbinary time signatures.')

    # make and return repeated skips
    return time_signature.numerator * Skip((1, time_signature.denominator))
