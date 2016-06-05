# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__containers__Tuplet_01():

    notes = scoretools.make_notes([0, 2, 4], (1, 8))
    target = scoretools.Tuplet(Multiplier(2, 3), notes)

    assert format(target) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
