# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__misc__version_string_01():
    r'''Version strings are ignored.
    '''

    target = Staff()
    string = r'''\version "2.14.2" \new Staff { }'''
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
