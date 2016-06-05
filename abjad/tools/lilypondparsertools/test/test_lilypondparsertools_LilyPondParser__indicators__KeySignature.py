# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__KeySignature_01():

    target = Staff([Note("fs'", 1)])
    key_signature = KeySignature('g', 'major')
    attach(key_signature, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            \key g \major
            fs'1
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    key_signatures = inspect_(result[0]).get_indicators(KeySignature)
    assert len(key_signatures) == 1
