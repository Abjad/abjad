from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.sequencetools import sum_consecutive_sequence_elements_by_sign


def milliseconds_to_q_events(milliseconds):
    '''Convert a list of millisecond durations to a list of
    :py:class:`~abjad.tools.quantizationtools.QEvent` objects.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched :py:class:`~abjad.tools.quantizationtools.QEvent` objects will
    default to using middle-C.

    ::

        abjad> from abjad.tools.quantizationtools import milliseconds_to_q_events
        abjad> durations = [100, -250, 500]
        abjad> milliseconds_to_q_events(durations)
        [QEvent(Offset(0, 1), 0), QEvent(Offset(100, 1), None), QEvent(Offset(350, 1), 0), QEvent(Offset(850, 1), None)]

    Return a list of :py:class:`~abjad.tools.quantizationtools.QEvent` objects.
    '''

    durations = filter(None, sum_consecutive_sequence_elements_by_sign(milliseconds, sign = [-1]))
    offsets = cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = QEvent(offset, None)
        else:
            q_event = QEvent(offset, 0)
        q_events.append(q_event)

    # insert terminating silence
    q_events.append(QEvent(Offset(offsets[-1]), None))

    return q_events
