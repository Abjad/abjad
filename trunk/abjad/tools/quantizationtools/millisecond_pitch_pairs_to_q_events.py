from collections import Iterable
from itertools import groupby
from numbers import Number
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent


def millisecond_pitch_pairs_to_q_events(pairs):
    '''Convert a list of pairs of millisecond durations and pitches to
    a list of :py:class:`~abjad.tools.quantizationtools.QEvent` instances.

    Pitch values must be one of the following:

    1. A single chromatic pitch number, indicating a note,
    2. None, indicating a silence, or
    3. An iterable of chromatic pitch numbers, indicating a chord.

    ::

        abjad> from abjad.tools.quantizationtools import millisecond_pitch_pairs_to_q_events
        abjad> durations = [1001, 503, 230, 1340]
        abjad> pitches = [None, 0, (1, 2, 3), 4.5]
        abjad> pairs = zip(durations, pitches)
        abjad> millisecond_pitch_pairs_to_q_events(pairs)
        [QEvent(Offset(0, 1), None), QEvent(Offset(1001, 1), 0), QEvent(Offset(1504, 1), (1, 2, 3)), QEvent(Offset(1734, 1), 4.5), QEvent(Offset(3074, 1), None)]

    Return a list of :py:class:`~abjad.tools.quantizationtools.QEvent` instances.
    '''

    # validate input
    assert isinstance(pairs, Iterable)
    assert all([isinstance(x, Iterable) for x in pairs])
    assert all([len(x) == 2 for x in pairs])
    assert all([0 < x[0] for x in pairs])
    for pair in pairs:
        assert isinstance(pair[1], (Number, type(None), Iterable))
        if isinstance(pair[1], Iterable):
            assert 0 < len(pair[1])
            assert all([isinstance(x, Number) for x in pair[1]])

    # fuse silences
    g = groupby(pairs, lambda x: x[1] is not None)
    groups = []
    for value, group in g:
        if value:
            groups.extend(list(group))
        else:
            duration = sum([x[0] for x in group])
            groups.append((duration, None))

    # find offsets
    offsets = cumulative_sums_zero([abs(x[0]) for x in groups])

    # build Q-events
    q_events = []
    for pair in zip(offsets, groups):
        offset = Offset(pair[0])
        # duration = abs(pair[1][0])
        pitches = pair[1][1]
        if isinstance(pitches, Iterable):
            assert all([isinstance(x, Number) for x in pitches])
        else:
            assert isinstance(pitches, (Number, type(None)))
        q_events.append(QEvent(offset, pitches))

    # add terminating silence
    q_events.append(QEvent(Offset(offsets[-1]), None))

    return q_events
