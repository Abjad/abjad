from abjad import *


def test_TempoMark___sub___01():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 4), 60)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    result = tempo_indication_1 - tempo_indication_2
    assert result == contexttools.TempoMark(Duration(1, 4), -30)

    result = tempo_indication_2 - tempo_indication_1
    assert result == contexttools.TempoMark(Duration(1, 4), 30)


def test_TempoMark___sub___02():

    tempo_indication_1 = contexttools.TempoMark(Duration(1, 8), 42)
    tempo_indication_2 = contexttools.TempoMark(Duration(1, 4), 90)

    result = tempo_indication_1 - tempo_indication_2
    assert result == contexttools.TempoMark(Duration(1, 4), -6)

    result = tempo_indication_2 - tempo_indication_1
    assert result == contexttools.TempoMark(Duration(1, 4), 6)
