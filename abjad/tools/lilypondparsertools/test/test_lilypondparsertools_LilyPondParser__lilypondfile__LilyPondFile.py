# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__lilypondfile__LilyPondFile_01():

    string = '{ c } { c } { c } { c }'
    parser = LilyPondParser()
    result = parser(string)
    assert isinstance(result, lilypondfiletools.LilyPondFile)
