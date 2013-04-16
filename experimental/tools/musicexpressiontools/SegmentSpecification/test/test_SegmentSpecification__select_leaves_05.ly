\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 2/8
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c'8.
				}
				{
					c'8.
				}
				{
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					c'16
				}
			}
		}
	>>
>>