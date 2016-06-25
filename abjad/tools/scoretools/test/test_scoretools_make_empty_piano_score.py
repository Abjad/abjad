# -*- coding: utf-8 -*-
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

    assert format(score) == stringtools.normalize(
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