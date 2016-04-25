# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_rhythmmakertools_TaleaRhythmMaker_read_talea_once_only_01():

    maker = rhythmmakertools.TaleaRhythmMaker(
        read_talea_once_only=True,
        talea=rhythmmakertools.Talea(
            counts=[1, 2, 3, 4],
            denominator=16,
            ),
        )

    divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
    string = 'maker(divisions)'
    assert pytest.raises(Exception, string)
