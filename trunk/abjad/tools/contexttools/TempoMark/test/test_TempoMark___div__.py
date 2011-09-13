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
