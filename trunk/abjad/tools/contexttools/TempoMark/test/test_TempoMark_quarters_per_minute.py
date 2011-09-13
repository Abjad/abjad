from abjad import *


def test_TempoMark_quarters_per_minute_01():
    '''Maelzel metronome marking with integer-valued mark.'''

    t = contexttools.TempoMark(Duration(3, 32), 52)
    assert t.quarters_per_minute == Duration(416, 3)


def test_TempoMark_quarters_per_minute_02():
    '''Maelzel metronome marking with float-valued mark.'''

    t = contexttools.TempoMark(Duration(3, 32), 52.5)
    assert t.quarters_per_minute == 140.0
