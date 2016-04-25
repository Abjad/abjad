# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo___add___01():

    tempo_1 = Tempo(Duration(1, 4), 60)
    tempo_2 = Tempo(Duration(1, 4), 90)

    result = tempo_1 + tempo_2
    assert result == Tempo(Duration(1, 4), 150)

    result = tempo_2 + tempo_1
    assert result == Tempo(Duration(1, 4), 150)


def test_indicatortools_Tempo___add___02():

    tempo_1 = Tempo(Duration(1, 8), 42)
    tempo_2 = Tempo(Duration(1, 4), 90)

    result = tempo_1 + tempo_2
    assert result == Tempo(Duration(1, 4), 174)

    result = tempo_2 + tempo_1
    assert result == Tempo(Duration(1, 4), 174)


def test_indicatortools_Tempo___add___03():

    tempo_1 = Tempo(textual_indication='Langsam')
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 + tempo_2"
    pytest.raises(ImpreciseTempoError, statement)


def test_indicatortools_Tempo___add___04():

    tempo_1 = Tempo(Duration(1, 8), (90, 92))
    tempo_2 = Tempo(Duration(1, 4), 90)

    statement = "tempo_1 + tempo_2"
    pytest.raises(ImpreciseTempoError, statement)
