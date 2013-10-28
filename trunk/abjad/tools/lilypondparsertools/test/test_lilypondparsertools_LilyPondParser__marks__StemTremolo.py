# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__StemTremolo_01():

    target = Staff([Note(0, 1)])
    stem_tremolo = marktools.StemTremolo(4)
    attach(stem_tremolo, target[0])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            c'1 :4
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    stem_tremolos = inspect(result[0]).get_marks(marktools.StemTremolo)
    assert 1 == len(stem_tremolos)
