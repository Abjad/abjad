import py.test
from abjad import *


def test_TempoMark___add___01():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 4), 60)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    result = tempo_indication_1 + tempo_indication_2
    assert result == contexttools.TempoMark(Duration(1, 4), 150)

    result = tempo_indication_2 + tempo_indication_1
    assert result == contexttools.TempoMark(Duration(1, 4), 150)


def test_TempoMark___add___02():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 8), 42)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    result = tempo_indication_1 + tempo_indication_2
    assert result == contexttools.TempoMark(Duration(1, 4), 174)

    result = tempo_indication_2 + tempo_indication_1
    assert result == contexttools.TempoMark(Duration(1, 4), 174)


def test_TempoMark___add___03():

    tempo_indication_1 = contexttools.TempoMark('Langsam')
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    py.test.raises(ImpreciseTempoError, "tempo_indication_1 + tempo_indication_2")


def test_TempoMark___add___04():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 8), (90, 92))
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    py.test.raises(ImpreciseTempoError, "tempo_indication_1 + tempo_indication_2")
