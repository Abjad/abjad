# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo___div___01():

    tempo_1 = Tempo(Duration(1, 4), 60)
    tempo_2 = Tempo(Duration(1, 4), 90)

    assert tempo_2 / tempo_1 == Duration(3, 2)
    assert tempo_1 / tempo_2 == Duration(2, 3)


def test_indicatortools_Tempo___div___02():

    tempo_1 = Tempo(Duration(1, 8), 42)
    tempo_2 = Tempo(Duration(1, 4), 90)

    assert tempo_2 / tempo_1 == Duration(15, 14)
    assert tempo_1 / tempo_2 == Duration(14, 15)


def test_indicatortools_Tempo___div___03():

    tempo_1 = Tempo(textual_indication='Langsam')
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 / tempo_2"
    pytest.raises(ImpreciseTempoError, statement)


def test_indicatortools_Tempo___div___04():

    tempo_1 = Tempo(Duration(1, 8), (90, 92))
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 / tempo_2"
    pytest.raises(ImpreciseTempoError, statement)
