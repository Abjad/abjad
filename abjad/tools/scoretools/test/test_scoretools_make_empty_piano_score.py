# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_make_empty_piano_score_01():

    score, treble, bass = scoretools.make_empty_piano_score()

    r'''
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
            }
            \context Staff = "bass" {
                \clef "bass"
            }
        >>
    >>
    '''

    assert inspect(score).is_well_formed()
    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                }
                \context Staff = "bass" {
                    \clef "bass"
                }
            >>
        >>
        '''
        )
