from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
    import tempo_scaled_rational_to_milliseconds
from abjad.tools.sequencetools import sum_consecutive_sequence_elements_by_sign


def tempo_scaled_rationals_to_q_events(durations, tempo):
    '''Convert a list of rational durations to a list of
    :py:class:`~abjad.tools.quantizationtools.QEvent` objects.

    Negative duration values can be used to indicate silence.  Any resulting
    pitched :py:class:`~abjad.tools.quantizationtools.QEvent` objects will
    default to using middle-C.

    ::

        abjad> from abjad.tools.quantizationtools import tempo_scaled_rationals_to_q_events
        abjad> durations = [Duration(-1, 2), Duration(1, 4), Duration(1, 6)]
        abjad> tempo = contexttools.TempoMark((1, 4), 55)
        abjad> tempo_scaled_rationals_to_q_events(durations, tempo)
        [QEvent(Offset(0, 1), None), QEvent(Offset(24000, 11), 0), QEvent(Offset(36000, 11), 0), QEvent(Duration(4000, 1), None)]

    Return a list of :py:class:`~abjad.tools.quantizationtools.QEvent` objects.
    '''

    assert all([isinstance(x, (int, Fraction)) for x in durations])
    assert isinstance(tempo, TempoMark)

    durations = filter(None, sum_consecutive_sequence_elements_by_sign(durations, sign = [-1]))
    durations = [tempo_scaled_rational_to_milliseconds(x, tempo) for x in durations]

    offsets = cumulative_sums_zero([abs(x) for x in durations])

    q_events = []
    for pair in zip(offsets, durations):
        offset = Offset(pair[0])
        duration = pair[1]
        if duration < 0: # negative duration indicates silence
            q_event = QEvent(offset, None)
        else: # otherwise, use middle-C
            q_event = QEvent(offset, 0)
        q_events.append(q_event)

    # insert terminating silence QEvent
    q_events.append(QEvent(offsets[-1], None))

    return q_events
