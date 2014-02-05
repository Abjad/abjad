# -*- encoding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker__split_sequence_extended_to_weights_01():

    maker = rhythmmakertools.TaleaRhythmMaker
    parts = maker._split_sequence_extended_to_weights(
        [1, 2, 3, 4, 5], 
        [7, 7, 7], 
        overhang=True,
        )

    assert parts == [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3], [4, 5]]


def test_rhythmmakertools_TaleaRhythmMaker__split_sequence_extended_to_weights_02():

    maker = rhythmmakertools.TaleaRhythmMaker
    parts = maker._split_sequence_extended_to_weights(
        [1, 2, 3, 4, 5], 
        [7, 7, 7], 
        overhang=False,
        )

    assert parts == [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3]]
