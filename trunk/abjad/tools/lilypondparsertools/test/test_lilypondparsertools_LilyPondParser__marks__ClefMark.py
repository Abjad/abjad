# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__ClefMark_01():
    target = Staff([Note(0, 1)])
    contexttools.ClefMark('bass')(target[0])

    r'''
    \new Staff {
        \clef "bass"
        c'1
    }
    '''

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
    clef_marks = inspect(result[0]).get_marks(contexttools.ClefMark)
    assert len(clef_marks) == 1
