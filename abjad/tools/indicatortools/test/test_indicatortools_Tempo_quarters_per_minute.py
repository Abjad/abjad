# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo_quarters_per_minute_01():
    r'''Maelzel metronome marking with integer.
    '''

    tempomark = Tempo(Duration(3, 32), 52)
    assert tempomark.quarters_per_minute == Duration(416, 3)


def test_indicatortools_Tempo_quarters_per_minute_02():
    r'''Maelzel metronome marking with float.
    '''

    tempomark = Tempo(Duration(3, 32), 52.5)
    assert tempomark.quarters_per_minute == 140.0
