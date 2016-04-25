# -*- coding: utf-8 -*-
from abjad.tools import lilypondparsertools


def test_lilypondparsertools_LilyPondParser_accidentals_forced_01():

    string = "{ c!4 }"
    parsed = lilypondparsertools.LilyPondParser()(string)

    assert parsed[0].note_head.is_forced == True
    assert format(parsed[0]) == 'c!4'


def test_lilypondparsertools_LilyPondParser_accidentals_forced_02():

    string = "{ <c! e g!!>4 }"
    parsed = lilypondparsertools.LilyPondParser()(string)

    assert parsed[0].note_heads[0].is_forced == True
    assert parsed[0].note_heads[1].is_forced == False
    assert parsed[0].note_heads[2].is_forced == True
    assert format(parsed[0]) == '<c! e g!>4'
