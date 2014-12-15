# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHead_is_parenthesized_01():

    note_head = scoretools.NoteHead(written_pitch="c'")
    assert note_head.is_parenthesized is None
    note_head.is_parenthesized = True
    assert note_head.is_parenthesized == True
    note_head.is_parenthesized = False
    assert note_head.is_parenthesized == False


def test_scoretools_NoteHead_is_parenthesized_01():

    note_head = scoretools.NoteHead(written_pitch="c'")
    note_head.is_parenthesized = True

    assert format(note_head) == systemtools.TestManager.clean_string(
        r'''
        \parenthesize
        c'
        ''')