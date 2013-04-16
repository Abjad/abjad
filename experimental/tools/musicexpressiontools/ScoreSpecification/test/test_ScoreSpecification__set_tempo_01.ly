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
		{
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					\tempo 4=90
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					\tempo 4=108
					c'8.
				}
				{
					c'8.
				}
				{
					c'8
				}
			}
		}
	>>
>>