# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__TimeSignature_01():

    target = Score([Staff([Note(0, 1)])])
    time_signature = TimeSignature((8, 8))
    attach(time_signature, target.select_leaves()[0])

    assert systemtools.TestManager.compare(
        target,
        r'''
        \new Score <<
            \new Staff {
                \time 8/8
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaf = result.select_leaves()[0]
    time_signatures = inspect_(leaf).get_indicators(TimeSignature)
    assert len(time_signatures) == 1
