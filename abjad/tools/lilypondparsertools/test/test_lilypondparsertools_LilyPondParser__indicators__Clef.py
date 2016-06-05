# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__Clef_01():

    target = Staff([Note(0, 1)])
    clef = Clef('bass')
    attach(clef, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "bass"
            c'1
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    clefs = inspect_(result[0]).get_indicators(Clef)
    assert len(clefs) == 1
