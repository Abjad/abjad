# -*- coding: utf-8 -*-
from abjad import *


def test_topleveltools_setting_01():
    r'''Works with score metronome mark interface.

    Does not include LilyPond \set command.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    setting(score).tempo_wholes_per_minute = schemetools.SchemeMoment(24)

    assert format(score) == String.normalize(
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


def test_topleveltools_setting_02():
    r'''Works with leaf metronome mark interface.

    Includes LilyPond \set command.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    moment = schemetools.SchemeMoment(24)
    leaves = select().by_leaf(flatten=True)(score)
    setting(leaves[1]).score.tempo_wholes_per_minute = moment

    assert format(score) == String.normalize(
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
