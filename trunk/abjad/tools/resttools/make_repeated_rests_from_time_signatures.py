from abjad.tools.resttools.make_repeated_rests_from_time_signature import make_repeated_rests_from_time_signature


def make_repeated_rests_from_time_signatures(time_signatures):
    '''.. versionadded 1.1.2

    Make repated rests from `time_signatures`::

        resttools.make_repeated_rests_from_time_signatures([(2, 8), (3, 32)])
        [[Rest('r8'), Rest('r8')], [Rest('r32'), Rest('r32'), Rest('r32')]]

    Return two-dimensional list of newly constructed rest lists.

    Use ``sequencetools.flatten_sequence()`` to flatten output if required.
    '''

    # init result
    result = []

    # iterate time signatures and make rests
    for time_signature in time_signatures:
        rests = make_repeated_rests_from_time_signature(time_signature)
        result.append(rests)

    # return result
    return result
