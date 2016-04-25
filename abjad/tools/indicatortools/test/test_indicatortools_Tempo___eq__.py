# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo___eq___01():
    r'''Tempos compare equal when durations and units per minute match.
    '''

    tempo_1 = Tempo(Duration(3, 32), 52)
    tempo_2 = Tempo(Duration(3, 32), 52)
    assert tempo_1 == tempo_2


def test_indicatortools_Tempo___eq___02():
    r'''Tempos do not compare equal when mathematically equal.
    '''

    tempo_1 = Tempo(Duration(3, 32), 52)
    tempo_2 = Tempo(Duration(6, 32), 104)
    assert not tempo_1 == tempo_2


def test_indicatortools_Tempo___eq___03():
    r'''Tempos also compare textual indications.
    '''

    tempo_1 = Tempo(Duration(3, 32), 52, 'Langsam')
    tempo_2 = Tempo(Duration(3, 32), 52, 'Langsam')
    tempo_3 = Tempo(Duration(3, 32), 52, 'Slow')
    assert tempo_1 == tempo_2

    assert not tempo_1 == tempo_3
