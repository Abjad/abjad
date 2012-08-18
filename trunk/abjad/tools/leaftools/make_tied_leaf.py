from abjad.tools import durationtools


def make_tied_leaf(kind, duration, big_endian=True, pitches=None, tied=True):
    '''Return list of leaves to fill the given duration `duration`.

    Leaves returned are tie-spanned when ``tied=True``.

    `duration`
        must be of the form ``m / 2**n`` for any integer ``m``.

    `big_endian` must be boolean.
        True returns a list of notes of decreasing duration.
        False returns a list of notes of increasing duration.

    `pitches`
        a pitch or list of pitch tokens.

    `tied`
        True to return tied leaves. False otherwise.
    '''
    from abjad.tools import tietools

    result = []
    for written_duration in durationtools.duration_token_to_assignable_duration_pairs(
        duration):
        if not pitches is None:
            args = (pitches, written_duration)
        else:
            args = (written_duration, )
        result.append(kind(*args))
    if 1 < len(result):
        if not big_endian:
            result.reverse()
        if tied:
            tietools.TieSpanner(result)
    return result
