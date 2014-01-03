% 2014-01-03 12:53

\version "2.18.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../stylesheets/gallery-layout.ly"

#(set-default-paper-size "letter" 'landscape)
#(set-global-staff-size 11)

\paper {
	tagline = \markup { }
}

\score {
	\new Score <<
		\context TimeSignatureContext = "TimeSignatureContext" {
			{
				\time 4/8
				s1 * 1/2
			}
			{
				\time 3/4
				s1 * 3/4
			}
			{
				\time 2/4
				s1 * 1/2
			}
			{
				\time 1/16
				s1 * 1/16
			}
			{
				s1 * 1/16
			}
			{
				\time 7/8
				s1 * 7/8
			}
			{
				\time 5/16
				s1 * 5/16
			}
		}
		\new RhythmicStaff {
			{
				\time 4/8
				{
					c'8 [
					c'8
					c'8
					c'8 ]
				}
			}
			{
				\time 3/4
				{
					c'4 [
					c'4
					c'4 ]
				}
			}
			{
				\time 2/4
				{
					c'4 [
					c'4 ]
				}
			}
			{
				\time 1/16
				{
					c'16 [ ]
				}
			}
			{
				{
					c'16 [ ]
				}
			}
			{
				\time 7/8
				{
					c'8 [
					c'8
					c'8
					c'8
					c'8
					c'8
					c'8 ]
				}
			}
			{
				\time 5/16
				{
					c'16 [
					c'16
					c'16
					c'16
					c'16 ]
				}
			}
		}
	>>
}

\score {
	\new Score <<
		\context TimeSignatureContext = "TimeSignatureContext" {
			{
				\time 4/8
				s1 * 1/2
			}
			{
				\time 3/4
				s1 * 3/4
			}
			{
				\time 2/4
				s1 * 1/2
			}
			{
				\time 1/16
				s1 * 1/16
			}
			{
				s1 * 1/16
			}
			{
				\time 7/8
				s1 * 7/8
			}
			{
				\time 5/16
				s1 * 5/16
			}
		}
		\new RhythmicStaff {
			{
				\time 4/8
				{
					c'16 [
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 3/4
				{
					c'8 [
					c'8
					c'8
					c'8
					c'8
					c'8 ]
				}
			}
			{
				\time 2/4
				{
					c'8 [
					c'8
					c'8
					c'8 ]
				}
			}
			{
				\time 1/16
				{
					c'32 [
					c'32 ]
				}
			}
			{
				{
					c'32 [
					c'32 ]
				}
			}
			{
				\time 7/8
				{
					c'16 [
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 5/16
				{
					c'32 [
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32 ]
				}
			}
		}
	>>
}

\score {
	\new Score <<
		\context TimeSignatureContext = "TimeSignatureContext" {
			{
				\time 4/8
				s1 * 1/2
			}
			{
				\time 3/4
				s1 * 3/4
			}
			{
				\time 2/4
				s1 * 1/2
			}
			{
				\time 1/16
				s1 * 1/16
			}
			{
				s1 * 1/16
			}
			{
				\time 7/8
				s1 * 7/8
			}
			{
				\time 5/16
				s1 * 5/16
			}
		}
		\new RhythmicStaff {
			{
				\time 4/8
				{
					c'32 [
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32 ]
				}
			}
			{
				\time 3/4
				{
					c'16 [
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 2/4
				{
					c'16 [
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 1/16
				{
					c'64 [
					c'64
					c'64
					c'64 ]
				}
			}
			{
				{
					c'64 [
					c'64
					c'64
					c'64 ]
				}
			}
			{
				\time 7/8
				{
					c'32 [
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32
					c'32 ]
				}
			}
			{
				\time 5/16
				{
					c'64 [
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64
					c'64 ]
				}
			}
		}
	>>
}