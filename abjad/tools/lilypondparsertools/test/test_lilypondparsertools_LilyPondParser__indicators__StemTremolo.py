# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__StemTremolo_01():

    target = Staff([Note(0, 1)])
    stem_tremolo = indicatortools.StemTremolo(4)
    attach(stem_tremolo, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c'1 :4
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    stem_tremolos = inspect_(result[0]).get_indicators(indicatortools.StemTremolo)
    assert 1 == len(stem_tremolos)
