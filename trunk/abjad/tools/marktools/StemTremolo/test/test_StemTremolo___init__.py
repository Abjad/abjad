from abjad import *


def test_StemTremolo___init___01():
    '''Initialize stem tremolo from tremolo flags.
    '''

    stem_tremolo = marktools.StemTremolo(16)
    assert isinstance(stem_tremolo, marktools.StemTremolo)


def test_StemTremolo___init___02():
    '''Initialize stem tremolo from other stem tremolo.
    '''

    stem_tremolo_1 = marktools.StemTremolo(16)
    stem_tremolo_2 = marktools.StemTremolo(stem_tremolo_1)

    assert isinstance(stem_tremolo_1, marktools.StemTremolo)
    assert isinstance(stem_tremolo_2, marktools.StemTremolo)
    assert stem_tremolo_1 == stem_tremolo_2
    assert stem_tremolo_1 is not stem_tremolo_2
