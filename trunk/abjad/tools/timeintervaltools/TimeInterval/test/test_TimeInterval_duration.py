from abjad.tools.timeintervaltools.TimeInterval import TimeInterval


def test_TimeInterval_duration_01():
    '''TimeInterval duration is the stop_offset minus the start_offset offset.
    '''
    i = TimeInterval(3, 23)
    assert (23 - 3) == i.duration
