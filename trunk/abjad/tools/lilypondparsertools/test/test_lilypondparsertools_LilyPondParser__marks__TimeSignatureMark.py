# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__TimeSignatureMark_01():

    target = Score([Staff([Note(0, 1)])])
    time_signature = contexttools.TimeSignatureMark((8, 8))
    time_signature.attach(target.select_leaves()[0])

    assert testtools.compare(
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
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    leaf = result.select_leaves()[0]
    time_signature_marks = \
        inspect(leaf).get_marks(contexttools.TimeSignatureMark)
    assert len(time_signature_marks) == 1
