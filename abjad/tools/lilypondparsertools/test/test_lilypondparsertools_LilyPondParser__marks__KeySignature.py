# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__KeySignature_01():

    target = Staff([Note("fs'", 1)])
    key_signature = marktools.KeySignature('g', 'major')
    attach(key_signature, target[0])

    assert systemtools.TestManager.compare(
        target,
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
    key_signatures = \
        inspect(result[0]).get_marks(marktools.KeySignature)
    assert len(key_signatures) == 1
