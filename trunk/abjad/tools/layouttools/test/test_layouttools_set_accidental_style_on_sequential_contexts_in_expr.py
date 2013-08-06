# -*- encoding: utf-8 -*-
from abjad import *


def test_layouttools_set_accidental_style_on_sequential_contexts_in_expr_01():

    score = Score(Staff("c'8 d'8") * 2)
    layouttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    r'''
    \new Score <<
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
    >>
    '''

    assert select(score).is_well_formed()
    assert testtools.compare(
        score.lilypond_format,
        r'''
        \new Score <<
            \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
            }
            \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
            }
        >>
        '''
        )


def test_layouttools_set_accidental_style_on_sequential_contexts_in_expr_02():
    r'''Skip nonsemantic contexts.
    '''

    score = Score(Staff("c'8 d'8") * 2)
    score[0].is_nonsemantic = True
    layouttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
        }
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
        }
    >>
    '''

    assert testtools.compare(
        score.lilypond_format,
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
            }
            \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
            }
        >>
        '''
        )
