# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection___illustrate___01():

    staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    selection = staff[2:6]
    lilypond_file = selection.__illustrate__()
    score = lilypond_file.score_block.items[0]

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                e'4
                f'4
                g'4
                a'4
            }
        >>
        '''
        )


def test_selectiontools_Selection___illustrate___02():

    staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    attach(Slur(), staff[:])
    selection = staff[2:6]
    lilypond_file = selection.__illustrate__()
    score = lilypond_file.score_block.items[0]

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                e'4 (
                f'4
                g'4
                a'4 )
            }
        >>
        '''
        )
