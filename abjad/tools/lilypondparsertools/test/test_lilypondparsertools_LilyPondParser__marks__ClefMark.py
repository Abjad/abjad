# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__marks__ClefMark_01():

    target = Staff([Note(0, 1)])
    clef = Clef('bass')
    attach(clef, target[0])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            \clef "bass"
            c'1
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    clef_marks = inspect(result[0]).get_marks(Clef)
    assert len(clef_marks) == 1
