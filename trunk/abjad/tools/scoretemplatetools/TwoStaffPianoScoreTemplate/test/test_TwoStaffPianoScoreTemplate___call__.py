# -*- encoding: utf-8 -*-
from abjad import *


def test_TwoStaffPianoScoreTemplate___call___01():

    template = scoretemplatetools.TwoStaffPianoScoreTemplate()
    score = template()

    r'''
    \context Score = "Two-Staff Piano Score" <<
        \context PianoStaff = "Piano Staff" <<
            \set PianoStaff.instrumentName = \markup { Piano }
            \set PianoStaff.shortInstrumentName = \markup { Pf. }
            \context Staff = "RH Staff" {
                \clef "treble"
                \context Voice = "RH Voice" {
                }
            }
            \context Staff = "LH Staff" {
                \clef "bass"
                \context Voice = "LH Voice" {
                }
            }
        >>
    >>
    '''

    assert testtools.compare(
        score.lilypond_format,
        r'''
        \context Score = "Two-Staff Piano Score" <<
            \context PianoStaff = "Piano Staff" <<
                \set PianoStaff.instrumentName = \markup { Piano }
                \set PianoStaff.shortInstrumentName = \markup { Pf. }
                \context Staff = "RH Staff" {
                    \clef "treble"
                    \context Voice = "RH Voice" {
                    }
                }
                \context Staff = "LH Staff" {
                    \clef "bass"
                    \context Voice = "LH Voice" {
                    }
                }
            >>
        >>
        '''
        )
