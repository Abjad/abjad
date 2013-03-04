from abjad.tools import durationtools
from abjad.tools import mathtools


def make_tied_leaf(kind, duration, decrease_durations_monotonically=True, 
    forbidden_written_duration=None, pitches=None, tie_parts=True):
    '''.. versionadded:: 1.0

    Make tied leaf of `kind` with assignable `duration`.

    `decrease_durations_monotonically` must be boolean.
        True returns a list of notes of decreasing duration.
        False returns a list of notes of increasing duration.

    `pitches`
        a pitch or list of pitches.

    `tie_parts`
        True to return tied leaves. False otherwise.
    '''
    from abjad.tools import tietools

    # check input
    duration = durationtools.Duration(duration)

    # make leaves
    result = []
    numerators = mathtools.partition_integer_into_canonic_parts(duration.numerator)
    if not decrease_durations_monotonically:
        numerators = list(reversed(numerators))
    for numerator in numerators:
        written_duration = durationtools.Duration(numerator, duration.denominator)
        if not pitches is None:
            args = (pitches, written_duration)
        else:
            args = (written_duration, )
        result.append(kind(*args))

    # apply tie spanner if required
    if tie_parts and 1 < len(result):
        tietools.TieSpanner(result)

    # return result
    return result
