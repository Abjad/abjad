# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_StemTremolo___init___01():
    r'''Initializes stem tremolo from tremolo flags.
    '''

    stem_tremolo = indicatortools.StemTremolo(16)
    assert isinstance(stem_tremolo, indicatortools.StemTremolo)


def test_indicatortools_StemTremolo___init___02():
    r'''Initializes stem tremolo from other stem tremolo.
    '''

    stem_tremolo_1 = indicatortools.StemTremolo(16)
    stem_tremolo_2 = indicatortools.StemTremolo(stem_tremolo_1)

    assert isinstance(stem_tremolo_1, indicatortools.StemTremolo)
    assert isinstance(stem_tremolo_2, indicatortools.StemTremolo)
    assert stem_tremolo_1 == stem_tremolo_2
    assert stem_tremolo_1 is not stem_tremolo_2
