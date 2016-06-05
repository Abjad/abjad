# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__functions__language_01():

    target = Container([
        Note("cs'8"),
        Note("ds'8"),
        Note("ff'8")
    ])

    assert format(target) == stringtools.normalize(
        r'''
        {
            cs'8
            ds'8
            ff'8
        }
        '''
        )

    string = r"\language nederlands { cis'8 dis'8 fes'8 }"
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
