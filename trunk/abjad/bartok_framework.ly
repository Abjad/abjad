% Abjad revision 3987
% 2010-10-19 01:05

\version "2.13.34"
\include "english.ly"
\include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

\header {
	tagline = \markup { "" }
}

\score {
	\new PianoStaff <<
		\new Staff {
			{
				\time 2/4
				a'8
				g'8
				f'8
				e'8
			}
			{
				\time 3/4
				d'4
				g'8
				f'8
				e'8
				d'8
			}
			{
				\time 2/4
				c'8
				d'16
				e'16
				f'8
				e'8
			}
			{
				\time 2/4
				d'2
			}
			{
				\time 2/4
				d'2
			}
		}
		\new Staff {
			{
				\time 2/4
				\context Voice = "main_voice" {
					b4
					d'8
					c'8
				}
			}
			{
				\time 3/4
				\context Voice = "main_voice" {
					b8
					a8
					af4
					c'8
					bf8
				}
			}
			{
				\time 2/4
				\context Voice = "main_voice" {
					a8
					g8
					fs8
					g16
					a16
				}
			}
			{
				\time 2/4
				<<
					\context Voice = "appendix_voice" {
						\voiceOne
						b2
					}
					\context Voice = "main_voice" {
						\voiceTwo
						b4
						a4
					}
				>>
			}
			{
				\time 2/4
				<<
					\context Voice = "appendix_voice" {
						\voiceOne
						b2
					}
					\context Voice = "main_voice" {
						\voiceTwo
						g2
					}
				>>
			}
		}
	>>
}