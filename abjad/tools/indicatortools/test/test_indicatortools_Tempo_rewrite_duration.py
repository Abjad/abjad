# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo_rewrite_duration_01():

    tempo_1 = Tempo(Duration(1, 4), 60)
    new_tempo = Tempo(Duration(1, 4), 90)

    result = tempo_1.rewrite_duration(Duration(1, 8), new_tempo)
    assert result == Duration(3, 16)

    result = tempo_1.rewrite_duration(Duration(1, 12), new_tempo)
    assert result == Duration(1, 8)

    result = tempo_1.rewrite_duration(Duration(1, 16), new_tempo)
    assert result == Duration(3, 32)

    result = tempo_1.rewrite_duration(Duration(1, 24), new_tempo)
    assert result == Duration(1, 16)
