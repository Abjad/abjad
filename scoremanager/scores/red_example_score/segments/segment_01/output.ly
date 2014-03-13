% 2014-03-13 17:54

\version "2.19.3"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/red-example-score-stylesheet.ily"

\header {}

\layout {}

\paper {}

\score {
	\context Score = "Two-Staff Piano Score" <<
		\context TimeSignatureContext = "Time Signature Context" {
			{
				\time 15/8
				s1 * 15/8
			}
			{
				\time 18/8
				s1 * 9/4
			}
		}
		\context PianoStaff = "Piano Staff" <<
			\set PianoStaff.instrumentName = \markup { Piano }
			\set PianoStaff.shortInstrumentName = \markup { Pf. }
			\context Staff = "RH Staff" {
				\clef "treble"
				\context Voice = "RH Voice" {
					g''4.
					bf''4.
					d''4.
					g'4.
					cs'8.
					af'8.
					a'8.
					e''8.
					bf''4 ~
					bf''16
					c'4 ~
					c'16
					fs'4 ~
					fs'16
					bf'4 ~
					bf'16
					a''4 ~
					a''16
					bf''4 ~
					bf''16
				}
			}
			\context Staff = "LH Staff" {
				\clef "bass"
				\context Voice = "LH Voice" {
					fs4 ~
					fs16
					d,4 ~
					d,16
					a4 ~
					a16
					g,4 ~
					g,16
					cs4 ~
					cs16
					a4 ~
					a16
					b,4.
					bf,4.
					c4.
					e,4.
					bf8.
					af,8.
					bf8.
					fs8.
				}
			}
		>>
	>>
}