# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_Scale_make_score_01():

    scale = tonalanalysistools.Scale('E', 'major')
    score = scale.make_score()

    assert format(score) == stringtools.normalize(
        r'''
        \new Score \with {
            tempoWholesPerMinute = #(ly:make-moment 30 1)
        } <<
            \new Staff {
                \key e \major
                e'8
                fs'8
                gs'8
                a'8
                b'8
                cs''8
                ds''8
                e''8
                ds''8
                cs''8
                b'8
                a'8
                gs'8
                fs'8
                e'4
            }
        >>
        '''
        )
