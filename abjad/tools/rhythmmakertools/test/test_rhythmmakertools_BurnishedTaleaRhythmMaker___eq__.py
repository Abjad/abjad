# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_BurnishedTaleaRhythmMaker___eq___01():

    maker_1 = rhythmmakertools.BurnishedTaleaRhythmMaker(
        talea=(-1, 2, -3, 4), 
        talea_denominator=16,
        prolation_addenda=(2, 3),
        secondary_divisions=(6,),
        )

    maker_2 = rhythmmakertools.BurnishedTaleaRhythmMaker(
        talea=(-1, 2, -3, 4), 
        talea_denominator=16,
        prolation_addenda=(2, 3),
        secondary_divisions=(6,),
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
