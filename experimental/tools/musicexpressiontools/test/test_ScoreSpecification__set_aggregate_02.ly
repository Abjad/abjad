\context Score = "Grouped Staves Score" <<
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
	\context StaffGroup = "Grouped Staves Staff Group" <<
		\context Staff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c8.
				}
				{
					cs'''8.
				}
				{
					d8.
				}
				{
					ef''8.
				}
				{
					e''8.
				}
				{
					f'8.
				}
				{
					fs'8
				}
			}
		}
	>>
>>