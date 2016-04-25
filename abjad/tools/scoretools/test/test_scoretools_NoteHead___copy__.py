# -*- coding: utf-8 -*-
from abjad import *
import copy


def test_scoretools_NoteHead___copy___01():

    note_head_1 = scoretools.NoteHead("cs''")
    note_head_1.is_cautionary = True
    note_head_1.is_forced = True
    note_head_1.tweak.color = 'red'
    note_head_1.tweak.font_size = -2

    note_head_2 = copy.copy(note_head_1)

    assert isinstance(note_head_1, scoretools.NoteHead)
    assert isinstance(note_head_2, scoretools.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
    assert note_head_1.is_cautionary == note_head_2.is_cautionary
    assert note_head_1.is_forced == note_head_2.is_forced
    assert note_head_1.tweak == note_head_2.tweak
    assert note_head_1.tweak is not note_head_2.tweak
