# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo___sub___01():

    tempo_1 = Tempo(Duration(1, 4), 60)
    tempo_2 = Tempo(Duration(1, 4), 90)

    result = tempo_1 - tempo_2
    assert result == Tempo(Duration(1, 4), -30)

    result = tempo_2 - tempo_1
    assert result == Tempo(Duration(1, 4), 30)


def test_indicatortools_Tempo___sub___02():

    tempo_1 = Tempo(Duration(1, 8), 42)
    tempo_2 = Tempo(Duration(1, 4), 90)

    result = tempo_1 - tempo_2
    assert result == Tempo(Duration(1, 4), -6)

    result = tempo_2 - tempo_1
    assert result == Tempo(Duration(1, 4), 6)


def test_indicatortools_Tempo___sub___03():

    tempo_1 = Tempo(textual_indication='Langsam')
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 - tempo_2"
    pytest.raises(ImpreciseTempoError, statement)


def test_indicatortools_Tempo___sub___04():

    tempo_1 = Tempo(Duration(1, 8), (90, 92))
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 - tempo_2"
    pytest.raises(ImpreciseTempoError, statement)
