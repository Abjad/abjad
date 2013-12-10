# -*- encoding: utf-8 -*-
from abjad import *


def test_templatetools_StringQuartetScoreTemplate___call___01():

    template = templatetools.StringQuartetScoreTemplate()
    score = template()

    r'''
    \context Score = "String Quartet Score" <<
        \context StaffGroup = "String Quartet Staff Group" <<
            \context Staff = "First Violin Staff" {
                \clef "treble"
                \set Staff.instrumentName = \markup { Violin }
                \set Staff.shortInstrumentName = \markup { Vn. }
                \context Voice = "First Violin Voice" {
                }
            }
            \context Staff = "Second Violin Staff" {
                \clef "treble"
                \set Staff.instrumentName = \markup { Violin }
                \set Staff.shortInstrumentName = \markup { Vn. }
                \context Voice = "Second Violin Voice" {
                }
            }
            \context Staff = "Viola Staff" {
                \clef "alto"
                \set Staff.instrumentName = \markup { Viola }
                \set Staff.shortInstrumentName = \markup { Va. }
                \context Voice = "Viola Voice" {
                }
            }
            \context Staff = "Cello Staff" {
                \clef "bass"
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
                \context Voice = "Cello Voice" {
                }
            }
        >>
    >>
    '''

    assert systemtools.TestManager.compare(
        score,
        r'''
        \context Score = "String Quartet Score" <<
            \context StaffGroup = "String Quartet Staff Group" <<
                \context Staff = "First Violin Staff" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "First Violin Voice" {
                    }
                }
                \context Staff = "Second Violin Staff" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Second Violin Voice" {
                    }
                }
                \context Staff = "Viola Staff" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola Voice" {
                    }
                }
                \context Staff = "Cello Staff" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello }
                    \set Staff.shortInstrumentName = \markup { Vc. }
                    \context Voice = "Cello Voice" {
                    }
                }
            >>
        >>
        '''
        )
