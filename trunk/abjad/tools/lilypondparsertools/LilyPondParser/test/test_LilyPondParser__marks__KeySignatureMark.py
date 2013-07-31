# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__KeySignatureMark_01():
    target = Staff([Note("fs'", 1)])
    contexttools.KeySignatureMark('g', 'major')(target[0])

    r'''
    \new Staff {
        \key g \major
        fs'1
    }
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    key_signature_marks = result[0].get_marks(contexttools.KeySignatureMark)
    assert len(key_signature_marks) == 1
