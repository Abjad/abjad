# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__TimeSignatureMark_01():
    target = Score([Staff([Note(0, 1)])])
    contexttools.TimeSignatureMark((8, 8))(target.select_leaves()[0])

    r'''
    \new Score <<
        \new Staff {
            \time 8/8
            c'1
        }
    >>
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    leaf = result.select_leaves()[0]
    time_signature_marks = inspect(leaf).get_marks(contexttools.TimeSignatureMark)
    assert len(time_signature_marks) == 1
