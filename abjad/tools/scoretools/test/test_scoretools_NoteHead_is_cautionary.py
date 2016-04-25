# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHead_is_cautionary_01():

    note_head = scoretools.NoteHead(written_pitch="c'")
    assert note_head.is_cautionary is None
    note_head.is_cautionary = True
    assert note_head.is_cautionary == True
    note_head.is_cautionary = False
    assert note_head.is_cautionary == False
