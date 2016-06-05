# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__misc__default_duration_01():

    target = Container(scoretools.make_notes([0],
        [(1, 4), (1, 2), (1, 2), (1, 8), (1, 8), (3, 16), (3, 16)]))
    attach(Multiplier(5, 17), target[-2])
    attach(Multiplier(5, 17), target[-1])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4
            c'2
            c'2
            c'8
            c'8
            c'8. * 5/17
            c'8. * 5/17
        }
        '''
        )

    string = r'''{ c' c'2 c' c'8 c' c'8. * 5/17 c' }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
