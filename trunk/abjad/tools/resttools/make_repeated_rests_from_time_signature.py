def make_repeated_rests_from_time_signature(time_signature):
    '''.. versionadded:: 2.0

    Make repeated rests from `time_signature`::

        >>> resttools.make_repeated_rests_from_time_signature((5, 32))
        [Rest('r32'), Rest('r32'), Rest('r32'), Rest('r32'), Rest('r32')]

    Return list of newly constructed rests.
    '''
    from abjad.tools import contexttools
    from abjad.tools import resttools

    # afford basic input polymorphism
    time_signature = contexttools.TimeSignatureMark(time_signature)

    # check input
    if time_signature.has_non_power_of_two_denominator:
        raise NotImplementedError(
            'TODO: extend this function for time signatures with non-power-of-two denominators.')

    # make and return repeated rests
    return time_signature.numerator * resttools.Rest((1, time_signature.denominator))
