import py.test
from abjad import *


def test_TempoMark___div___01():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 4), 60)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    assert tempo_indication_2 / tempo_indication_1 == Duration(3, 2)
    assert tempo_indication_1 / tempo_indication_2 == Duration(2, 3)


def test_TempoMark___div___02():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 8), 42)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    assert tempo_indication_2 / tempo_indication_1 == Duration(15, 14)
    assert tempo_indication_1 / tempo_indication_2 == Duration(14, 15)


def test_TempoMark___div___03():

    tempo_indication_1 = contexttools.TempoMark('Langsam')
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    py.test.raises(ImpreciseTempoError, "tempo_indication_1 / tempo_indication_2")


def test_TempoMark___div___04():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 8), (90, 92))
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    py.test.raises(ImpreciseTempoError, "tempo_indication_1 / tempo_indication_2")


