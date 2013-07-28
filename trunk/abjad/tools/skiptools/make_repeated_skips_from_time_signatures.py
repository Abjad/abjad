def make_repeated_skips_from_time_signatures(time_signatures):
    '''Make repeated skips from `time_signatures`:

    ::

        skiptools.make_repeated_skips_from_time_signatures([(2, 8), (3, 32)])
        [[Skip('s8'), Skip('s8')], [Skip('s32'), Skip('s32'), Skip('s32')]]

    Return two-dimensional list of newly constructed skip lists.
    '''
    from abjad.tools import skiptools

    # init result
    result = []

    # iterate time signatures and make skips
    for time_signature in time_signatures:
        skips = _make_repeated_skips_from_time_signature(time_signature)
        result.append(skips)

    # return result
    return result


def _make_repeated_skips_from_time_signature(time_signature):
    from abjad.tools import skiptools

    # afford basic input polymorphism
    time_signature = contexttools.TimeSignatureMark(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        message = 'TODO: extend this function for time signatures'
        message += ' with non-power-of-two denominators.'
        raise NotImplementedError(message)

    # make and return repeated skips
    skip = skiptools.Skip((1, time_signature.denominator))
    return time_signature.numerator * skip
