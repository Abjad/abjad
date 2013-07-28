def make_repeated_rests_from_time_signatures(time_signatures):
    '''Make repeated rests from `time_signatures`:

    ::

        resttools.make_repeated_rests_from_time_signatures([(2, 8), (3, 32)])
        [[Rest('r8'), Rest('r8')], [Rest('r32'), Rest('r32'), Rest('r32')]]

    Return two-dimensional list of newly constructed rest lists.

    Use ``sequencetools.flatten_sequence()`` to flatten output if required.
    '''
    from abjad.tools import resttools

    # initialize result
    result = []

    # iterate time signatures and make rests
    for time_signature in time_signatures:
        rests = _make_repeated_rests_from_time_signature(time_signature)
        result.append(rests)

    # return result
    return result


def _make_repeated_rests_from_time_signature(time_signature):
    from abjad.tools import contexttools
    from abjad.tools import resttools

    # afford basic input polymorphism
    time_signature = contexttools.TimeSignatureMark(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        message = 'TODO: extend this function for time signatures'
        message += ' with non-power-of-two denominators.'
        raise NotImplementedError(message)

    # make and return repeated rests
    rest = resttools.Rest((1, time_signature.denominator))
    return time_signature.numerator * rest
