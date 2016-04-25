# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker___eq___01():

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )
    maker_1 = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(2, 3),
        split_divisions_by_counts=(6,),
        )

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )
    maker_2 = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(2, 3),
        split_divisions_by_counts=(6,),
        )

    assert maker_1 == maker_1
    assert maker_1 == maker_2
    assert not maker_1 == 'foo'
    assert maker_2 == maker_1
    assert maker_2 == maker_2
    assert not maker_2 == 'foo'
    assert not 'foo' == maker_1
    assert not 'foo' == maker_2
    assert 'foo' == 'foo'
