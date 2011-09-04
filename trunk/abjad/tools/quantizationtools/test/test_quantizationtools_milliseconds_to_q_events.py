from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import difference_series
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import milliseconds_to_q_events
from abjad.tools.quantizationtools._time_segments import _time_segments


def test_quantizationtools_milliseconds_to_q_events_01():
    '''Test basic functionality.'''

    durations = difference_series([x[0] for x in _time_segments])
    q_events = milliseconds_to_q_events(durations)

    assert q_events == [
        QEvent(Offset(0, 1), 0),
        QEvent(Offset(163, 1), 0),
        QEvent(Offset(511, 1), 0),
        QEvent(Offset(627, 1), 0),
        QEvent(Offset(1208, 1), 0),
        QEvent(Offset(1417, 1), 0),
        QEvent(Offset(1997, 1), 0),
        QEvent(Offset(3204, 1), 0),
        QEvent(Offset(3297, 1), 0),
        QEvent(Offset(4087, 1), 0),
        QEvent(Offset(4296, 1), 0),
        QEvent(Offset(4830, 1), 0),
        QEvent(Offset(6362, 1), 0),
        QEvent(Offset(6595, 1), 0),
        QEvent(Offset(6687, 1), 0),
        QEvent(Offset(7013, 1), 0),
        QEvent(Offset(7245, 1), 0),
        QEvent(Offset(7872, 1), 0),
        QEvent(Offset(8197, 1), 0),
        QEvent(Offset(8359, 1), 0),
        QEvent(Offset(8638, 1), 0),
        QEvent(Offset(8731, 1), 0),
        QEvent(Offset(8917, 1), 0),
        QEvent(Offset(9288, 1), 0),
        QEvent(Offset(9404, 1), 0),
        QEvent(Offset(10240, 1), 0),
        QEvent(Offset(10356, 1), 0),
        QEvent(Offset(10496, 1), 0),
        QEvent(Offset(10890, 1), 0),
        QEvent(Offset(11169, 1), 0),
        QEvent(Offset(11285, 1), 0),
        QEvent(Offset(11424, 1), 0),
        QEvent(Offset(12307, 1), 0),
        QEvent(Offset(12957, 1), 0),
        QEvent(Offset(13073, 1), 0),
        QEvent(Offset(13653, 1), 0),
        QEvent(Offset(13979, 1), 0),
        QEvent(Offset(14234, 1), 0),
        QEvent(Offset(15256, 1), 0),
        QEvent(Offset(15883, 1), 0),
        QEvent(Offset(16022, 1), 0),
        QEvent(Offset(16649, 1), 0),
        QEvent(Offset(16927, 1), 0),
        QEvent(Offset(17044, 1), 0),
        QEvent(Offset(17276, 1), 0),
        QEvent(Offset(18483, 1), None)]

def test_quantizationtools_milliseconds_to_q_events_02():
    '''Silences are fused.'''

    durations = [100, -100, 100, -100, -100, 100]
    q_events = milliseconds_to_q_events(durations)
    assert q_events == [
        QEvent(0, 0),
        QEvent(100, None),
        QEvent(200, 0),
        QEvent(300, None),
        QEvent(500, 0),
        QEvent(600, None)]
