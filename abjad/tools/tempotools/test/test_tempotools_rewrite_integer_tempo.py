# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.mathtools import Ratio


def test_tempotools_rewrite_integer_tempo_03():

    pairs = tempotools.rewrite_integer_tempo(
        52, 
        maximum_numerator=4, 
        maximum_denominator=4,
        )

    assert pairs == [
        (26, Ratio(1, 2)), 
        (39, Ratio(3, 4)), 
        (52, Ratio(1, 1)), 
        (78, Ratio(3, 2)), 
        (104, Ratio(2, 1)),
        ]


def test_tempotools_rewrite_integer_tempo_04():

    pairs = tempotools.rewrite_integer_tempo(
        52, 
        maximum_numerator=8, 
        maximum_denominator=8,
        )

    assert pairs == [
        (26, Ratio(1, 2)), 
        (39, Ratio(3, 4)), 
        (52, Ratio(1, 1)), 
        (65, Ratio(5, 4)), 
        (78, Ratio(3, 2)), 
        (91, Ratio(7, 4)), 
        (104, Ratio(2, 1)),
        ]
