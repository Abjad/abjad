# -*- encoding: utf-8 -*-
from abjad import *


def test_TempoMark_quarters_per_minute_01():
    r'''Maelzel metronome marking with integer-valued mark.
    '''

    tempomark = contexttools.TempoMark(Duration(3, 32), 52)
    assert tempomark.quarters_per_minute == Duration(416, 3)


def test_TempoMark_quarters_per_minute_02():
    r'''Maelzel metronome marking with float-valued mark.
    '''

    t = contexttools.TempoMark(Duration(3, 32), 52.5)
    assert t.quarters_per_minute == 140.0
