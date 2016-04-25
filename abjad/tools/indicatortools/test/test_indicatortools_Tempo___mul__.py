# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo___mul___01():

    tempo = Tempo(Duration(1, 4), 60)
    result = tempo * Duration(1, 2)
    assert result == Tempo(Duration(1, 4), 30)

    result = tempo * Duration(2, 3)
    assert result == Tempo(Duration(1, 4), 40)

    result = tempo * Duration(3, 4)
    assert result == Tempo(Duration(1, 4), 45)

    result = tempo * Duration(4, 5)
    assert result == Tempo(Duration(1, 4), 48)

    result = tempo * Duration(5, 6)
    assert result == Tempo(Duration(1, 4), 50)

    result = tempo * Duration(6, 7)
    assert result == Tempo(
        Duration(1, 4), Duration(360, 7))


def test_indicatortools_Tempo___mul___02():

    tempo = Tempo(Duration(1, 4), 60)
    result = tempo * 1
    assert result == Tempo(Duration(1, 4), 60)

    result = tempo * 2
    assert result == Tempo(Duration(1, 4), 120)

    result = tempo * 3
    assert result == Tempo(Duration(1, 4), 180)

    result = tempo * 4
    assert result == Tempo(Duration(1, 4), 240)


def test_indicatortools_Tempo___mul___03():

    tempo_1 = Tempo(textual_indication='Langsam')
    pytest.raises(ImpreciseTempoError, "tempo_1 * Duration(1, 2)")


def test_indicatortools_Tempo___mul___04():

    tempo_1 = Tempo(Duration(1, 8), (90, 92))
    pytest.raises(ImpreciseTempoError, "tempo_1 * Duration(1, 2)")
