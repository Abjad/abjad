# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__contexts__with_blocks_01():

    target = Staff([])

    r'''
    \new Staff {
    }
    '''

    string = r'''\new Staff \with { } {
    }
    '''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
