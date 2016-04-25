# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHead_is_forced_01():

    note_head = scoretools.NoteHead(written_pitch="c'")
    assert note_head.is_forced is None
    note_head.is_forced = True
    assert note_head.is_forced == True
    note_head.is_forced = False
    assert note_head.is_forced == False
