# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__KeySignatureMark_01():

    target = Staff([Note("fs'", 1)])
    key_signature = marktools.KeySignatureMark('g', 'major')
    attach(key_signature, target[0])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            \key g \major
            fs'1
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    key_signature_marks = \
        inspect(result[0]).get_marks(marktools.KeySignatureMark)
    assert len(key_signature_marks) == 1
