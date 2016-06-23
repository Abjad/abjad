# -*- coding: utf-8 -*-
from abjad import *


def test_topleveltools_set__01():
    r'''Works with score tempo interface.
    Does not include LilyPond \set command.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    set_(score).tempo_wholes_per_minute = schemetools.SchemeMoment(24)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score \with {
            tempoWholesPerMinute = #(ly:make-moment 24 1)
        } <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        '''
        )


def test_topleveltools_set__02():
    r'''Works with leaf tempo interface. Includes LilyPond \set command.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    moment = schemetools.SchemeMoment(24)
    leaves = select().by_leaf(flatten=True)(score)
    set_(leaves[1]).score.tempo_wholes_per_minute = moment

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'8
                \set Score.tempoWholesPerMinute = #(ly:make-moment 24 1)
                d'8
                e'8
                f'8
            }
        >>
        '''
        )