from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.quantizationtools.PitchedQEvent import PitchedQEvent
from experimental.quantizationtools.TerminalQEvent import TerminalQEvent
from experimental.quantizationtools.UnpitchedQEvent import UnpitchedQEvent


def milliseconds_to_q_events(milliseconds):
    '''Convert a list of millisecond durations to a list of
    :py:class:`~abjad.tools.quantizationtools.QEvent` objects.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched :py:class:`~abjad.tools.quantizationtools.QEvent` objects will
    default to using middle-C.

    ::

        >>> from experimental.quantizationtools import milliseconds_to_q_events
        >>> durations = [100, -250, 500]
        >>> milliseconds_to_q_events(durations)
        [QEvent(Offset(0, 1), 0), QEvent(Offset(100, 1), None), QEvent(Offset(350, 1), 0), QEvent(Offset(850, 1), None)]

    Return a list of :py:class:`~abjad.tools.quantizationtools.QEvent` objects.
    '''

    durations = [x for x in sequencetools.sum_consecutive_sequence_elements_by_sign(milliseconds, sign=[-1]) if x]
    offsets = mathtools.cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = durationtools.Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = UnpitchedQEvent(offset)
        else:
            q_event = PitchedQEvent(offset, [0])
        q_events.append(q_event)

    q_events.append(TerminalQEvent(durationtools.Offset(offsets[-1])))

    return q_events
