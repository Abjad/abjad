# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_NoteRhythmMaker___eq___01():

    maker_1 = rhythmmakertools.NoteRhythmMaker()
    maker_2 = rhythmmakertools.NoteRhythmMaker()

    assert maker_1 == maker_2
    assert maker_2 == maker_1
    assert not maker_1 == 'foo'
