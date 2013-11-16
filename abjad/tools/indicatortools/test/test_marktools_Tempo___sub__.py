# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo___sub___01():

    tempo_indication_1 = Tempo(Duration(1, 4), 60)
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    result = tempo_indication_1 - tempo_indication_2
    assert result == Tempo(Duration(1, 4), -30)

    result = tempo_indication_2 - tempo_indication_1
    assert result == Tempo(Duration(1, 4), 30)


def test_indicatortools_Tempo___sub___02():

    tempo_indication_1 = Tempo(Duration(1, 8), 42)
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    result = tempo_indication_1 - tempo_indication_2
    assert result == Tempo(Duration(1, 4), -6)

    result = tempo_indication_2 - tempo_indication_1
    assert result == Tempo(Duration(1, 4), 6)


def test_indicatortools_Tempo___sub___03():

    tempo_indication_1 = Tempo('Langsam')
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    pytest.raises(ImpreciseTempoError, "tempo_indication_1 - tempo_indication_2")


def test_indicatortools_Tempo___sub___04():

    tempo_indication_1 = Tempo(Duration(1, 8), (90, 92))
    tempo_indication_2 = Tempo(Duration(1, 4), 90)

    pytest.raises(ImpreciseTempoError, "tempo_indication_1 - tempo_indication_2")
