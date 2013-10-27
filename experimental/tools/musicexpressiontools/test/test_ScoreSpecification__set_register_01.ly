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
		{
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Staves Staff Group" <<
		\context Staff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c''16
				}
				{
					cs''16
				}
				{
					d''16
				}
				{
					ef''16
				}
				{
					e''16
				}
				{
					f''16
				}
				{
					fs''16
				}
				{
					g16
				}
				{
					af''16
				}
				{
					a''16
				}
				{
					bf''16
				}
				{
					b16
				}
				{
					c''16
				}
				{
					cs''16
				}
				{
					d''16
				}
				{
					ef''16
				}
				{
					e''16
				}
				{
					f''16
				}
				{
					fs''16
				}
				{
					g16
				}
				{
					af''16
				}
				{
					a''16
				}
				{
					bf''16
				}
				{
					b16
				}
			}
		}
	>>
>>