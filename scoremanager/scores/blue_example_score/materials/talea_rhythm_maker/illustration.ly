% 2014-07-07 09:29

\version "2.19.8"
\language "english"

#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 12)

\header {}

\layout {
	\accidentalStyle forget
	indent = #0
	ragged-right = ##t
	\context {
		\name TimeSignatureContext
		\type Engraver_group
		\consists Axis_group_engraver
		\consists Time_signature_engraver
		\override TimeSignature #'X-extent = #'(0 . 0)
		\override TimeSignature #'X-offset = #ly:self-alignment-interface::x-aligned-on-self
		\override TimeSignature #'Y-extent = #'(0 . 0)
		\override TimeSignature #'break-align-symbol = ##f
		\override TimeSignature #'break-visibility = #end-of-line-invisible
		\override TimeSignature #'font-size = #1
		\override TimeSignature #'self-alignment-X = #center
		\override VerticalAxisGroup #'default-staff-staff-spacing = #'((basic-distance . 0) (minimum-distance . 10) (padding . 6) (stretchability . 0))
	}
	\context {
		\Score
		\remove Bar_number_engraver
		\accepts TimeSignatureContext
		\override Beam #'breakable = ##t
		\override SpacingSpanner #'strict-grace-spacing = ##t
		\override SpacingSpanner #'strict-note-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t
		\override TupletBracket #'bracket-visibility = ##t
		\override TupletBracket #'minimum-length = #3
		\override TupletBracket #'padding = #2
		\override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
		\override TupletNumber #'text = #tuplet-number::calc-fraction-text
		autoBeaming = ##f
		proportionalNotationDuration = #(ly:make-moment 1 32)
		tupletFullLength = ##t
	}
	\context {
		\StaffGroup
	}
	\context {
		\Staff
		\remove Time_signature_engraver
	}
	\context {
		\RhythmicStaff
		\remove Time_signature_engraver
	}
}

\paper {
	left-margin = #20
	system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
}

\score {
	\new Score <<
		\new TimeSignatureContext {
			{
				\time 3/8
				s1 * 3/8
			}
			{
				\time 4/8
				s1 * 1/2
			}
			{
				\time 3/16
				s1 * 3/16
			}
			{
				\time 4/16
				s1 * 1/4
			}
		}
		\new RhythmicStaff {
			{
				\time 3/8
				\times 2/3 {
					c'4
					c'8 ~
				}
				{
					c'8
				}
			}
			{
				\time 4/8
				\times 2/3 {
					r4.
				}
				{
					c'8 ~
				}
				{
					c'8
				}
			}
			{
				\time 3/16
				{
					c'8 ~
				}
				{
					c'16 ~
				}
			}
			{
				\time 4/16
				{
					c'16
				}
				\tweak #'text #tuplet-number::calc-fraction-text
				\times 3/5 {
					r4
					r16
				}
			}
		}
	>>
}