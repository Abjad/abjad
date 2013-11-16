# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.mathtools import Ratio


def test_indicatortools_Tempo_list_related_tempos_01():

    tempo = Tempo(Duration(1, 4), 52)
    pairs = tempo.list_related_tempos(
        maximum_numerator=4, 
        maximum_denominator=4,
        )

    assert pairs == [
        (Tempo(Duration(1, 4), 26), Ratio(1, 2)), 
        (Tempo(Duration(1, 4), 39), Ratio(3, 4)), 
        (Tempo(Duration(1, 4), 52), Ratio(1, 1)),
        ]


def test_indicatortools_Tempo_list_related_tempos_02():

    tempo = Tempo(Duration(1, 4), 52)
    pairs = tempo.list_related_tempos(
        maximum_numerator=8, 
        maximum_denominator=8,
        )

    assert pairs == [
        (Tempo(Duration(1, 4), 26), Ratio(1, 2)), 
        (Tempo(Duration(1, 4), 39), Ratio(3, 4)), 
        (Tempo(Duration(1, 4), 52), Ratio(1, 1)), 
        (Tempo(Duration(1, 4), 65), Ratio(5, 4)), 
        (Tempo(Duration(1, 4), 78), Ratio(3, 2)),
        (Tempo(Duration(1, 4), 91), Ratio(7, 4)), 
        (Tempo(Duration(1, 4), 104), Ratio(2, 1)),
        ]
