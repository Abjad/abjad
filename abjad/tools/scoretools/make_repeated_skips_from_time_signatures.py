# -*- coding: utf-8 -*-
from abjad.tools import selectiontools


def make_repeated_skips_from_time_signatures(time_signatures):
    r'''Make repeated skips from `time_signatures`:

    ::

        scoretools.make_repeated_skips_from_time_signatures([(2, 8), (3, 32)])
        [Selection(Skip('s8'), Skip('s8')), Selection(Skip('s32'), Skip('s32'), Skip('s32'))]

    Returns two-dimensional list of newly constructed skip lists.
    '''
    from abjad.tools import scoretools

    # init result
    result = []

    # iterate time signatures and make skips
    for time_signature in time_signatures:
        skips = _make_repeated_skips_from_time_signature(time_signature)
        result.append(skips)

    # return result
    return result


def _make_repeated_skips_from_time_signature(time_signature):
    from abjad.tools import scoretools

    # afford basic input polymorphism
    time_signature = indicatortools.TimeSignature(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        message = 'TODO: extend this function for time signatures'
        message += ' with non-power-of-two denominators.'
        raise NotImplementedError(message)

    # make and return repeated skips
    skip = scoretools.Skip((1, time_signature.denominator))
    skips = time_signature.numerator * skip
    result = selectiontools.Selection(skips)
