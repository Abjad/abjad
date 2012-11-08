from abjad.tools import durationtools
from abjad.tools import mathtools


def make_tied_leaf(kind, duration, decrease_durations_monotonically=True, pitches=None, tied=True):
    '''Return list of leaves to fill the given duration `duration`.

    Leaves returned are tie-spanned when ``tied=True``.

    `duration`
        must be of the form ``m / 2**n`` for any integer ``m``.

    `decrease_durations_monotonically` must be boolean.
        True returns a list of notes of decreasing duration.
        False returns a list of notes of increasing duration.

    `pitches`
        a pitch or list of pitch tokens.

    `tied`
        True to return tied leaves. False otherwise.
    '''
    from abjad.tools import tietools

    # check input
    duration = durationtools.Duration(duration)

    result = []
    for numerator in mathtools.partition_integer_into_canonic_parts(duration.numerator):
        written_duration = durationtools.Duration(numerator, duration.denominator)
        if not pitches is None:
            args = (pitches, written_duration)
        else:
            args = (written_duration, )
        result.append(kind(*args))

    if 1 < len(result):
        if not decrease_durations_monotonically:
            result.reverse()
        if tied:
            tietools.TieSpanner(result)

    return result
