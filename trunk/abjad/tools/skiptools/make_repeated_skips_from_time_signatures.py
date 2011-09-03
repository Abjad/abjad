from abjad.tools.skiptools.make_repeated_skips_from_time_signature import make_repeated_skips_from_time_signature


def make_repeated_skips_from_time_signatures(time_signatures):
    '''.. versionadded 1.1.2

    Make repated skips from `time_signatures`::

        skiptools.make_repeated_skips_from_time_signatures([(2, 8), (3, 32)])
        [[Skip('s8'), Skip('s8')], [Skip('s32'), Skip('s32'), Skip('s32')]]

    Return list of skip lists.
    '''

    # init result
    result = []

    # iterate time signatures and make skips
    for time_signature in time_signatures:
        skips = make_repeated_skips_from_time_signature(time_signature)
        result.append(skips)

    # return result
    return result
