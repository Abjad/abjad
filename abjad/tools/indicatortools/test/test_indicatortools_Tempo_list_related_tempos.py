# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo_list_related_tempos_01():

    tempo = Tempo(Duration(1, 4), 52)
    pairs = tempo.list_related_tempos(
        maximum_numerator=4, 
        maximum_denominator=4,
        )

    assert pairs == [
        (Tempo(Duration(1, 4), 26), mathtools.Ratio(1, 2)), 
        (Tempo(Duration(1, 4), 39), mathtools.Ratio(3, 4)), 
        (Tempo(Duration(1, 4), 52), mathtools.Ratio(1, 1)),
        ]


def test_indicatortools_Tempo_list_related_tempos_02():

    tempo = Tempo(Duration(1, 4), 52)
    pairs = tempo.list_related_tempos(
        maximum_numerator=8, 
        maximum_denominator=8,
        )

    assert pairs == [
        (Tempo(Duration(1, 4), 26), mathtools.Ratio(1, 2)), 
        (Tempo(Duration(1, 4), 39), mathtools.Ratio(3, 4)), 
        (Tempo(Duration(1, 4), 52), mathtools.Ratio(1, 1)), 
        (Tempo(Duration(1, 4), 65), mathtools.Ratio(5, 4)), 
        (Tempo(Duration(1, 4), 78), mathtools.Ratio(3, 2)),
        (Tempo(Duration(1, 4), 91), mathtools.Ratio(7, 4)), 
        (Tempo(Duration(1, 4), 104), mathtools.Ratio(2, 1)),
        ]
