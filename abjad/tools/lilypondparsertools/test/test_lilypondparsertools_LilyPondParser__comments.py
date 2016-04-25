# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__comments_01():

    target = Container([Note(0, (1, 4))])

    string = r'''
    { c'4 }
    % { d'4 }
    % { e'4 }'''  # NOTE: no newline should follow the final brace

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result)
