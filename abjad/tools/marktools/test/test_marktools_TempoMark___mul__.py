# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_TempoMark___mul___01():

    tempo_indication = TempoMark(Duration(1, 4), 60)
    result = tempo_indication * Duration(1, 2)
    assert result == TempoMark(Duration(1, 4), 30)

    result = tempo_indication * Duration(2, 3)
    assert result == TempoMark(Duration(1, 4), 40)

    result = tempo_indication * Duration(3, 4)
    assert result == TempoMark(Duration(1, 4), 45)

    result = tempo_indication * Duration(4, 5)
    assert result == TempoMark(Duration(1, 4), 48)

    result = tempo_indication * Duration(5, 6)
    assert result == TempoMark(Duration(1, 4), 50)

    result = tempo_indication * Duration(6, 7)
    assert result == TempoMark(
        Duration(1, 4), Duration(360, 7))


def test_TempoMark___mul___02():

    tempo_indication = TempoMark(Duration(1, 4), 60)
    result = tempo_indication * 1
    assert result == TempoMark(Duration(1, 4), 60)

    result = tempo_indication * 2
    assert result == TempoMark(Duration(1, 4), 120)

    result = tempo_indication * 3
    assert result == TempoMark(Duration(1, 4), 180)

    result = tempo_indication * 4
    assert result == TempoMark(Duration(1, 4), 240)


def test_TempoMark___mul___03():

    tempo_indication_1 = TempoMark('Langsam')
    pytest.raises(ImpreciseTempoError, "tempo_indication_1 * Duration(1, 2)")


def test_TempoMark___mul___04():

    tempo_indication_1 = TempoMark(Duration(1, 8), (90, 92))
    pytest.raises(ImpreciseTempoError, "tempo_indication_1 * Duration(1, 2)")
