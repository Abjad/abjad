# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__functions__grace_01():

    target = Container([
        Note("c'4"),
        Note("d'4"),
        Note("e'2")
    ])

    grace = scoretools.GraceContainer([
        Note("g''16"),
        Note("fs''16")
    ])

    attach(grace, target[2])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4
            d'4
            \grace {
                g''16
                fs''16
            }
            e'2
        }
        '''
        )

    string = r"{ c'4 d'4 \grace { g''16 fs''16} e'2 }"
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
