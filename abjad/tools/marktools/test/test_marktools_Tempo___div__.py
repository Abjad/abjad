# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_TempoMark___div___01():

    tempo_indication_1 = Tempo(Duration(1, 4), 60)
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    assert tempo_indication_2 / tempo_indication_1 == Duration(3, 2)
    assert tempo_indication_1 / tempo_indication_2 == Duration(2, 3)


def test_TempoMark___div___02():

    tempo_indication_1 = Tempo(Duration(1, 8), 42)
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    assert tempo_indication_2 / tempo_indication_1 == Duration(15, 14)
    assert tempo_indication_1 / tempo_indication_2 == Duration(14, 15)


def test_TempoMark___div___03():

    tempo_indication_1 = Tempo('Langsam')
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    pytest.raises(ImpreciseTempoError, "tempo_indication_1 / tempo_indication_2")


def test_TempoMark___div___04():

    tempo_indication_1 = Tempo(Duration(1, 8), (90, 92))
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    pytest.raises(ImpreciseTempoError, "tempo_indication_1 / tempo_indication_2")
