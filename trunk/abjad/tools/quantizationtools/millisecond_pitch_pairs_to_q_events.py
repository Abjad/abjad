import collections
import itertools
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools


def millisecond_pitch_pairs_to_q_events(pairs):
    '''Convert a list of pairs of millisecond durations and pitches to
    a list of ``QEvent`` instances.

    Pitch values must be one of the following:

    1. A single chromatic pitch number, indicating a note,
    2. None, indicating a silence, or
    3. An iterable of chromatic pitch numbers, indicating a chord.

    ::

        >>> durations = [1001, 503, 230, 1340]
        >>> pitches = [None, 0, (1, 2, 3), 4.5]
        >>> pairs = zip(durations, pitches)
        >>> for x in quantizationtools.millisecond_pitch_pairs_to_q_events(pairs): x
        ...
        quantizationtools.SilentQEvent(
            durationtools.Offset(0, 1),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1001, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1504, 1),
            (NamedChromaticPitch("cs'"), NamedChromaticPitch("d'"), NamedChromaticPitch("ef'")),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1734, 1),
            (NamedChromaticPitch("eqs'"),),
            attachments=()
            )
        quantizationtools.TerminalQEvent(
            durationtools.Offset(3074, 1)
            )

    Return a list of ``QEvent`` instances.
    '''
    from experimental import quantizationtools

    # validate input
    assert isinstance(pairs, collections.Iterable)
    assert all([isinstance(x, collections.Iterable) for x in pairs])
    assert all([len(x) == 2 for x in pairs])
    assert all([0 < x[0] for x in pairs])
    for pair in pairs:
        assert isinstance(pair[1], (numbers.Number, type(None), collections.Iterable))
        if isinstance(pair[1], collections.Iterable):
            assert 0 < len(pair[1])
            assert all([isinstance(x, numbers.Number) for x in pair[1]])

    # fuse silences
    g = itertools.groupby(pairs, lambda x: x[1] is not None)
    groups = []
    for value, group in g:
        if value:
            groups.extend(list(group))
        else:
            duration = sum([x[0] for x in group])
            groups.append((duration, None))

    # find offsets
    offsets = mathtools.cumulative_sums_zero([abs(x[0]) for x in groups])

    # build QEvents
    q_events = []
    for pair in zip(offsets, groups):

        offset = durationtools.Offset(pair[0])
        pitches = pair[1][1]

        if isinstance(pitches, collections.Iterable):
            assert all([isinstance(x, numbers.Number) for x in pitches])
            q_events.append(quantizationtools.PitchedQEvent(offset, pitches))
        elif isinstance(pitches, type(None)):
            q_events.append(quantizationtools.SilentQEvent(offset))
        elif isinstance(pitches, numbers.Number):
            q_events.append(quantizationtools.PitchedQEvent(offset, [pitches]))

    q_events.append(quantizationtools.TerminalQEvent(durationtools.Offset(offsets[-1])))

    return q_events
