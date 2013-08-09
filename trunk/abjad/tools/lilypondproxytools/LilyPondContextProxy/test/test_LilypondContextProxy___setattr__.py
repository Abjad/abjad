# -*- encoding: utf-8 -*-
from abjad import *


def test_LilypondContextProxy___setattr___01():
    r'''Works with score tempo interface.
    Does not include LilyPond \set command.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    score.set.tempo_wholes_per_minute = schemetools.SchemeMoment(24)

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

    assert testtools.compare(
        score,
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


def test_LilypondContextProxy___setattr___02():
    r'''Works with leaf tempo interface.
    Includes LilyPond \set command.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    score.select_leaves()[1].set.score.tempo_wholes_per_minute = schemetools.SchemeMoment(24)

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

    assert testtools.compare(
        score,
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
